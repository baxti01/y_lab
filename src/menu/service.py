import uuid
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src import models
from src.database import get_session
from src.menu import schemas


class MenuService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_menus(self) -> List[schemas.FullMenu]:
        result = []
        menus = (
            self.session.query(models.Menu)
            .options(
                joinedload(models.Menu.submenus)
                .joinedload(models.Submenu.dishes)
            )
            .all()
        )

        for menu in menus:
            submenu_count = len(menu.submenus)
            dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

            item = schemas.FullMenu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenu_count=submenu_count,
                dishes_count=dishes_count
            )

            result.append(item)

        return result

    def get_menu(
            self,
            menu_id: uuid.UUID
    ) -> models.Menu:
        menu = (
            self.session.query(models.Menu)
            .filter_by(id=menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                detail="menu not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return menu

    def create_menu(
            self,
            data: schemas.BaseMenu
    ) -> models.Menu:
        menu = models.Menu(**data.model_dump())
        try:
            self.session.add(menu)
            self.session.commit()
        except Exception as e:
            raise HTTPException(
                detail="Ошибка создания меню",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return menu

    def patch_menu(
            self,
            meu_id: uuid.UUID,
            data: schemas.UpdateMenu
    ) -> models.Menu:
        menu = self.get_menu(meu_id)
        for field, value in data:
            setattr(menu, field, value)

        self.session.commit()
        self.session.refresh(menu)

        return menu

    def delete_menu(
            self,
            menu_id: uuid.UUID
    ) -> None:
        menu = self.get_menu(menu_id)
        self.session.delete(menu)
        self.session.commit()
