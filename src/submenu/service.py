import uuid
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src import models
from src.database import get_session
from src.submenu import schemas
from src.submenu.schemas import UpdateSubmenu


class SubmenuService:

    def __init__(
            self, session: Session = Depends(get_session)
    ):
        self.session = session

    def get_submenus(
            self,
            menu_id: uuid.UUID
    ) -> List[models.Submenu]:
        result = []

        submenus = (
            self.session.query(models.Submenu)
            .filter_by(menu_id=menu_id)
            .options(
                joinedload(models.Submenu.dishes)
            )
            .all()
        )

        for submenu in submenus:
            item = schemas.FullSubmenu(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                dishes_count=len(submenu.dishes)
            )

            result.append(item)

        return result

    def get_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> models.Submenu:
        submenu = (
            self.session.query(models.Submenu)
            .filter_by(
                id=submenu_id,
                menu_id=menu_id
            )
            .first()
        )

        if not submenu:
            raise HTTPException(
                detail="submenu not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return submenu

    def create_submenu(
            self,
            menu_id: uuid.UUID,
            data: schemas.BaseSubmenu
    ) -> models.Submenu:
        menu = self.session.query(models.Menu).get(menu_id)

        if not menu:
            raise HTTPException(
                detail="menu not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        submenu = models.Submenu(
            **data.model_dump(),
            menu_id=menu_id
        )

        self.session.add(submenu)
        self.session.commit()

        return submenu

    def patch_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: UpdateSubmenu
    ) -> models.Submenu:
        submenu = self.get_submenu(menu_id, submenu_id)

        for field, value in data:
            setattr(submenu, field, value)

        self.session.commit()
        self.session.refresh(submenu)

        return submenu

    def delete_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> None:
        submenu = self.get_submenu(menu_id, submenu_id)

        self.session.delete(submenu)
        self.session.commit()
