import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.database import get_session
from src.menu import schemas
from src.menu.repository import MenuRepository
from src.redis.repository import RedisRepository


class MenuService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.menu_repository = MenuRepository(session=session)
        self.redis_repository = RedisRepository()

    @classmethod
    async def _merge_data(
            cls,
            instance: models.Menu,
            submenus_count: int,
            dishes_count: int,
    ) -> schemas.Menu:
        menu = schemas.Menu.model_validate(instance)
        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        return menu

    async def get_menus(self) -> list[schemas.Menu]:
        result = []
        cached_data = await self.redis_repository.get_data(
            keys=[self.get_menus.__name__],
            model=schemas.Menu
        )
        if cached_data:
            return cached_data

        for menu_tuple in await self.menu_repository.get_all():
            result.append(await self._merge_data(*menu_tuple))

        await self.redis_repository.set_data(
            keys=[self.get_menus.__name__],
            data=result,
            expire=180
        )

        return result

    async def get_menu(
            self,
            menu_id: uuid.UUID
    ) -> schemas.Menu:
        cached_data = await self.redis_repository.get_data(
            keys=[self.get_menu.__name__, menu_id],
            model=schemas.Menu
        )
        if cached_data:
            return cached_data[0]

        db_data = await self._merge_data(
            *await self.menu_repository.get(id=menu_id)
        )
        await self.redis_repository.set_data(
            keys=[self.get_menu.__name__, menu_id],
            data=[db_data],
            expire=180
        )

        return db_data

    async def create_menu(
            self,
            created_data: schemas.CreateMenu
    ) -> schemas.Menu:
        cached_data = await self.redis_repository.get_data(
            keys=[self.create_menu.__name__],
            model=schemas.Menu
        )
        if cached_data:
            return cached_data[0]

        db_data = await self._merge_data(
            *await self.menu_repository.create(created_data)
        )

        await self.redis_repository.set_data(
            keys=[self.create_menu.__name__],
            data=[db_data],
            expire=180
        )
        await self.redis_repository.invalidate_cache(
            keys=[self.get_menus.__name__]

        )

        return db_data

    async def patch_menu(
            self,
            menu_id: uuid.UUID,
            patched_data: schemas.UpdateMenu
    ) -> schemas.Menu:
        cached_data = await self.redis_repository.get_data(
            keys=[self.patch_menu.__name__, menu_id],
            model=schemas.Menu
        )
        if cached_data:
            return cached_data[0]

        db_data = await self._merge_data(
            *await self.menu_repository.patch(
                menu_id=menu_id,
                data=patched_data
            )
        )

        await self.redis_repository.set_data(
            keys=[self.patch_menu.__name__, menu_id],
            data=[db_data],
            expire=180
        )

        # Удаляет сразу несколько ключей
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [self.get_menus.__name__],
                [menu_id],
                [self.create_menu.__name__],
            ]
        )

        return db_data

    async def delete_menu(
            self,
            menu_id: uuid.UUID
    ) -> None:
        await self.menu_repository.delete(menu_id)

        # Удаляет сразу несколько ключей
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [self.get_menus.__name__],
                [menu_id],
                [self.create_menu.__name__],
                [self.patch_menu.__name__],
            ]
        )
