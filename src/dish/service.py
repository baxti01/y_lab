import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.database import get_session
from src.dish import schemas
from src.dish.repository import DishRepository
from src.menu.service import MenuService
from src.redis.repository import RedisRepository
from src.submenu.repository import SubmenuRepository


class DishService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session
        self.dish_repository = DishRepository(session)
        self.submenu_repository = SubmenuRepository(session)
        self.redis_repository = RedisRepository()

    async def get_dishes(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> list[schemas.Dish] | list[models.Dish]:
        cached_data = await self.redis_repository.get_data(
            keys=[self.get_dishes.__name__, menu_id, submenu_id],
            model=schemas.Dish
        )
        if cached_data:
            return cached_data

        data = await self.dish_repository.get_all(menu_id, submenu_id)

        await self.redis_repository.set_data(
            keys=[self.get_dishes.__name__, menu_id, submenu_id],
            data=data,
            expire=180
        )

        return data

    async def get_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID

    ) -> schemas.Dish | models.Dish:
        cached_data = await self.redis_repository.get_data(
            keys=[
                self.get_dish.__name__, menu_id,
                submenu_id, dish_id
            ],
            model=schemas.Dish
        )
        if cached_data:
            return cached_data[0]

        data = await self.dish_repository.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )
        await self.redis_repository.set_data(
            keys=[
                self.get_dish.__name__, menu_id,
                submenu_id, dish_id
            ],
            data=[data],
            expire=180
        )

        return data

    async def create_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            created_data: schemas.CreateDish
    ) -> schemas.Dish | models.Dish:
        await self.submenu_repository.get(menu_id, id=submenu_id)
        cached_data = await self.redis_repository.get_data(
            keys=[self.create_dish.__name__, menu_id, submenu_id],
            model=models.Dish
        )

        if cached_data:
            return cached_data[0]

        db_data = await self.dish_repository.create(
            menu_id=menu_id,
            submenu_id=submenu_id,
            data=created_data
        )
        await self.redis_repository.set_data(
            keys=[self.create_dish.__name__, menu_id, submenu_id],
            data=[db_data],
            expire=180
        )

        # Удаляем из кэша все что было связано с menu_id,
        # submenu_id и get_menus что бы новое блюдо учитывалось
        # при подсчёте количество подменю и блюд
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )

        return db_data

    async def patch_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            patched_data: schemas.UpdateDish
    ) -> schemas.Dish | models.Dish:
        cached_data = await self.redis_repository.get_data(
            keys=[self.patch_dish.__name__, menu_id,
                  submenu_id, dish_id],
            model=schemas.Dish
        )
        if cached_data:
            return cached_data[0]

        db_data = await self.dish_repository.patch(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            data=patched_data
        )
        await self.redis_repository.set_data(
            keys=[self.patch_dish.__name__, menu_id,
                  submenu_id, dish_id],
            data=[db_data],
            expire=180
        )

        # Удаляем из кэша все что было связано с menu_id,
        # submenu_id и get_menus что бы новое блюдо учитывалось
        # при подсчёте количество подменю и блюд
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )

        return db_data

    async def delete_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID
    ) -> None:
        await self.dish_repository.delete(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )

        # Удаляем из кэша все что было связано с menu_id,
        # submenu_id и get_menus что бы новое блюдо учитывалось
        # при подсчёте количество подменю и блюд
        await self.redis_repository.invalidate_caches(
            caches_keys=[
                [menu_id],
                [MenuService.get_menus.__name__]
            ]
        )
