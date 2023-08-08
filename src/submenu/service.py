import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from src import models
from src.database import get_session
from src.menu.repository import MenuRepository
from src.submenu import schemas
from src.submenu.repository import SubmenuRepository
from src.submenu.schemas import UpdateSubmenu


class SubmenuService:

    def __init__(
            self, session: Session = Depends(get_session)
    ):
        self.session = session,
        self.submenu_repository = SubmenuRepository(session)
        self.menu_repository = MenuRepository(session)

    @classmethod
    def _merge_data(
            cls,
            instance: models.Submenu,
            dishes_count: int
    ) -> schemas.Submenu:
        submenu = schemas.Submenu.model_validate(instance)
        submenu.dishes_count = dishes_count

        return submenu

    def get_submenus(
            self,
            menu_id: uuid.UUID
    ) -> list[schemas.Submenu]:
        result = []
        for submenu_tuple in self.submenu_repository.get_all(menu_id):
            result.append(self._merge_data(*submenu_tuple))

        return result

    def get_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> schemas.Submenu:
        return self._merge_data(
            *self.submenu_repository.get(
                menu_id=menu_id,
                id=submenu_id
            )
        )

    def create_submenu(
            self,
            menu_id: uuid.UUID,
            data: schemas.CreateSubmenu
    ) -> schemas.Submenu:
        # checking the menu availability
        self.menu_repository.get(id=menu_id)

        return self._merge_data(
            *self.submenu_repository.create(menu_id, data)
        )

    def patch_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: UpdateSubmenu
    ) -> schemas.Submenu:
        return self._merge_data(
            *self.submenu_repository.patch(
                menu_id=menu_id,
                submenu_id=submenu_id,
                data=data
            )
        )

    def delete_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> None:
        self.submenu_repository.delete(menu_id, submenu_id)
