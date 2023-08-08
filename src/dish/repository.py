import uuid

from fastapi import HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src import models
from src.dish.schemas import CreateDish, UpdateDish


class DishRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> list[models.Dish]:
        query = self.session.execute(
            select(models.Dish)
            .outerjoin(models.Submenu, models.Submenu.menu_id == menu_id)
            .where(models.Dish.submenu_id == submenu_id)
        )

        return query.scalars()

    def get(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            **kwargs
    ) -> models.Dish:
        query = self.session.execute(
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

    def create(
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
        dish = self.session.execute(stmt)
        self.session.commit()

        return self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish.scalar_one()
        )

    def patch(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: UpdateDish
    ) -> models.Dish:
        dish = self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )

        for field, value in data:
            setattr(dish, field, value)

        self.session.commit()
        self.session.refresh(dish)

        return dish

    def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> None:
        dish = self.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )

        self.session.delete(dish)
        self.session.commit()
