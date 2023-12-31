import uuid

from fastapi import HTTPException, status
from sqlalchemy import and_, delete, distinct, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.submenu import schemas


class SubmenuRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
            self,
            menu_id: uuid.UUID
    ) -> list[tuple[models.Submenu, int]]:
        query = await self.session.execute(
            select(
                models.Submenu,
                func.count(distinct(models.Dish.id))
            )
            .outerjoin(models.Dish, models.Dish.submenu_id == models.Submenu.id)
            .where(models.Submenu.menu_id == menu_id)
            .group_by(models.Submenu.id)
        )

        return query.all()

    async def get(
            self,
            menu_id: uuid.UUID,
            **kwargs
    ) -> tuple[models.Submenu, int]:
        query = await self.session.execute(
            select(
                models.Submenu,
                func.count(distinct(models.Dish.id))
            )
            .filter_by(menu_id=menu_id, **kwargs)
            .outerjoin(models.Dish, models.Dish.submenu_id == models.Submenu.id)
            .group_by(models.Submenu.id)
        )

        submenu = query.first()
        if not submenu:
            raise HTTPException(
                detail='submenu not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return submenu

    async def create(
            self,
            menu_id: uuid.UUID,
            data: schemas.CreateSubmenu
    ) -> tuple[models.Submenu, int]:
        stmt = insert(models.Submenu).values(
            **data.model_dump(),
            id=uuid.uuid4(),
            menu_id=menu_id
        ).returning(models.Submenu.id)

        submenu = await self.session.execute(stmt)
        await self.session.commit()

        return await self.get(
            menu_id=menu_id,
            id=submenu.scalar_one()
        )

    async def patch(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: schemas.UpdateSubmenu
    ) -> tuple[models.Submenu, int]:
        submenu = await self.get(
            menu_id=menu_id,
            id=submenu_id
        )

        for field, value in data:
            setattr(submenu[0], field, value)

        await self.session.commit()
        await self.session.refresh(submenu[0])

        return submenu

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> None:
        stmt = delete(models.Submenu).where(
            and_(
                models.Submenu.menu_id == menu_id,
                models.Submenu.id == submenu_id
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
