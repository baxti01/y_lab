import uuid

from fastapi import HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.dish.schemas import CreateDish, UpdateDish


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> list[models.Dish]:
        query = await self.session.execute(
            select(models.Dish)
            .outerjoin(models.Submenu, models.Submenu.menu_id == menu_id)
            .where(models.Dish.submenu_id == submenu_id)
        )

        return query.scalars().fetchall()

    async def get(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            **kwargs
    ) -> models.Dish:
        query = await self.session.execute(
            select(models.Dish)
            .filter_by(submenu_id=submenu_id, **kwargs)
            .outerjoin(models.Submenu, models.Submenu.menu_id == menu_id)
            .group_by(models.Dish.id)
        )

        dish = query.scalar()

        if not dish:
            raise HTTPException(
                detail='dish not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return dish

    async def create(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: CreateDish
    ) -> models.Dish:
        stmt = insert(models.Dish).values(
            **data.model_dump(),
            id=uuid.uuid4(),
            submenu_id=submenu_id
        ).returning(models.Dish.id)
        dish = await self.session.execute(stmt)
        await self.session.commit()

        return await self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish.scalar_one()
        )

    async def patch(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: UpdateDish
    ) -> models.Dish:
        dish = await self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )

        for field, value in data:
            setattr(dish, field, value)

        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> None:
        dish = await self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )

        await self.session.delete(dish)
        await self.session.commit()
