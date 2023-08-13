import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.database import get_session
from src.menu.repository import MenuRepository
from src.menu.service import MenuService
from src.redis.repository import RedisRepository
from src.submenu import schemas
from src.submenu.repository import SubmenuRepository
from src.submenu.schemas import UpdateSubmenu


class SubmenuService:

    def __init__(
            self, session: AsyncSession = Depends(get_session)
    ):
        self.session = session,
        self.submenu_repository = SubmenuRepository(session)
        self.menu_repository = MenuRepository(session)
        self.redis_repository = RedisRepository()

    @classmethod
    async def _merge_data(
            cls,
            instance: models.Submenu,
            dishes_count: int
    ) -> schemas.Submenu:
        submenu = schemas.Submenu.model_validate(instance)
        submenu.dishes_count = dishes_count

        return submenu

    async def get_submenus(
            self,
            menu_id: uuid.UUID
    ) -> list[schemas.Submenu]:
        result = []
        cached_data = await self.redis_repository.get_data(
            keys=[self.get_submenus.__name__, menu_id],
            model=schemas.Submenu
        )
        if cached_data:
            return cached_data

        for submenu_tuple in await self.submenu_repository.get_all(menu_id):
            result.append(await self._merge_data(*submenu_tuple))

        await self.redis_repository.set_data(
            keys=[self.get_submenus.__name__, menu_id],
            data=result,
            expire=180
        )

        return result

    async def get_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> schemas.Submenu:
        cached_data = await self.redis_repository.get_data(
            keys=[self.get_submenu.__name__, menu_id, submenu_id],
            model=schemas.Submenu
        )
        if cached_data:
            return cached_data[0]

        data = await self._merge_data(
            *await self.submenu_repository.get(
                menu_id=menu_id,
                id=submenu_id
            )
        )
        await self.redis_repository.set_data(
            keys=[self.get_submenu.__name__, menu_id, submenu_id],
            data=[data],
            expire=180
        )

        return data

    async def create_submenu(
            self,
            menu_id: uuid.UUID,
            created_data: schemas.CreateSubmenu
    ) -> schemas.Submenu:
        # checking the menu availability
        await self.menu_repository.get(id=menu_id)
        cached_data = await self.redis_repository.get_data(
            keys=[self.create_submenu.__name__, menu_id],
            model=schemas.Submenu
        )
        if cached_data:
            return cached_data[0]

        db_data = await self._merge_data(
            *await self.submenu_repository.create(menu_id, created_data)
        )

        await self.redis_repository.set_data(
            keys=[self.create_submenu.__name__, menu_id],
            data=[db_data],
            expire=180
        )

        # Удаляем из кэща все что было связано с menu_id
        # и get_menus что бы новое подменю учитывалось
        # при подсчёты количество подменю
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )

        return db_data

    async def patch_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            patched_data: UpdateSubmenu
    ) -> schemas.Submenu:
        cached_data = await self.redis_repository.get_data(
            keys=[self.patch_submenu.__name__, menu_id,
                  submenu_id, patched_data],
            model=schemas.Submenu
        )
        if cached_data:
            return cached_data[0]

        db_data = await self._merge_data(
            *await self.submenu_repository.patch(
                menu_id=menu_id,
                submenu_id=submenu_id,
                data=patched_data
            )
        )

        await self.redis_repository.set_data(
            keys=[self.patch_submenu.__name__, menu_id, submenu_id],
            data=[db_data],
            expire=180
        )

        # Удаляем из кэша все что было связано с menu_id
        # и get_menus что бы новое подменю учитывалось
        # при подсчёты количество подменю
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )

        return db_data

    async def delete_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> None:
        await self.submenu_repository.delete(menu_id, submenu_id)

        # Удаляем из кэша все что было связано с menu_id
        # и get_menus что бы новое подменю учитывалось в
        # при подсчёты количество подменю
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )
