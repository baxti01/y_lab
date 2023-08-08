import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from src import models
from src.database import get_session
from src.dish import schemas
from src.dish.repository import DishRepository
from src.submenu.repository import SubmenuRepository


class DishService:

    def __init__(
            self,
            session: Session = Depends(get_session)
    ):
        self.session = session
        self.dish_repository = DishRepository(session)
        self.submenu_repository = SubmenuRepository(session)

    def get_dishes(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> list[models.Dish]:
        return self.dish_repository.get_all(menu_id, submenu_id)

    def get_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID

    ) -> models.Dish:
        return self.dish_repository.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )

    def create_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: schemas.CreateDish
    ) -> models.Dish:
        self.submenu_repository.get(menu_id, id=submenu_id)

        return self.dish_repository.create(
            menu_id=menu_id,
            submenu_id=submenu_id,
            data=data
        )

    def patch_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: schemas.UpdateDish
    ) -> models.Dish:
        return self.dish_repository.patch(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            data=data
        )

    def delete_dish(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID
    ) -> None:
        self.dish_repository.delete(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )
