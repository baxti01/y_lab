import uuid
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import models
from src.database import get_session
from src.dish import schemas


class DishService:

    def __init__(
            self,
            session: Session = Depends(get_session)
    ):
        self.session = session

    def get_dishes(
            self,
            submenu_id: uuid.UUID
    ) -> List[models.Dish]:
        dishes = (
            self.session.query(models.Dish)
            .filter_by(
                submenu_id=submenu_id
            )
            .all()
        )

        return dishes

    def get_dish(
            self,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID

    ) -> models.Dish:
        dish = (
            self.session.query(models.Dish)
            .filter_by(
                id=dish_id,
                submenu_id=submenu_id
            )
            .first()
        )

        if not dish:
            raise HTTPException(
                detail="dish not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return dish

    def create_dish(
            self,
            submenu_id: uuid.UUID,
            data: schemas.CreateDish
    ) -> models.Dish:
        submenu = self.session.query(models.Submenu).get(submenu_id)

        if not submenu:
            raise HTTPException(
                detail="submenu not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        dish = models.Dish(
            id=uuid.uuid4(),
            **data.model_dump(),
            submenu_id=submenu_id
        )

        try:
            self.session.add(dish)
            self.session.commit()
        except Exception as e:
            raise HTTPException(
                detail=f"{e.args} \n ss {e}",
                status_code=400
            )

        return dish

    def patch_dish(
            self,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: schemas.UpdateDish
    ) -> models.Dish:
        dish = self.get_dish(submenu_id, dish_id)

        for field, value in data:
            setattr(dish, field, value)

        self.session.commit()
        self.session.refresh(dish)

        return dish

    def delete_dish(
            self,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID
    ) -> None:
        dish = self.get_dish(submenu_id, dish_id)

        self.session.delete(dish)
        self.session.commit()
