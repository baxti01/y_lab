import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from src import models
from src.database import get_session
from src.menu import schemas
from src.menu.repository import MenuRepository


class MenuService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.menu_repository = MenuRepository(session=session)

    @classmethod
    def _merge_data(
            cls,
            instance: models.Menu,
            submenus_count: int,
            dishes_count: int,
    ) -> schemas.Menu:
        menu = schemas.Menu.model_validate(instance)
        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        return menu

    def get_menus(self) -> list[schemas.Menu]:
        result = []
        for menu_tuple in self.menu_repository.get_all():
            result.append(self._merge_data(*menu_tuple))

        return result

    def get_menu(
            self,
            menu_id: uuid.UUID
    ) -> schemas.Menu:
        return self._merge_data(
            *self.menu_repository.get(id=menu_id)
        )

    def create_menu(
            self,
            data: schemas.CreateMenu
    ) -> schemas.Menu:
        return self._merge_data(
            *self.menu_repository.create(data)
        )

    def patch_menu(
            self,
            menu_id: uuid.UUID,
            data: schemas.UpdateMenu
    ) -> schemas.Menu:
        return self._merge_data(
            *self.menu_repository.patch(
                menu_id=menu_id,
                data=data
            )
        )

    def delete_menu(
            self,
            menu_id: uuid.UUID
    ) -> None:
        self.menu_repository.delete(menu_id)
