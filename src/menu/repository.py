import uuid

from fastapi import HTTPException, status
from sqlalchemy import delete, distinct, func, insert, select
from sqlalchemy.orm import Session

from src import models
from src.menu import schemas


class MenuRepository:
    model = models.Menu

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[tuple[models.Menu, int, int]]:
        query = self.session.execute(
            select(
                models.Menu,
                func.count(distinct(models.Submenu.id)).label('submenus_count'),
                func.count(distinct(models.Dish.id)).label('dishes_count')
            )
            .outerjoin(models.Submenu, models.Menu.id == models.Submenu.menu_id)
            .outerjoin(models.Dish, models.Submenu.id == models.Dish.submenu_id)
            .group_by(models.Menu.id)
        )

        return query.all()

    def get(
            self,
            **kwargs
    ) -> tuple[models.Menu, int, int]:
        query = self.session.execute(
            select(
                models.Menu,
                func.count(distinct(models.Submenu.id)).label('submenus_count'),
                func.count(distinct(models.Dish.id)).label('dishes_count')
            )
            .filter_by(**kwargs)
            .outerjoin(models.Submenu, models.Menu.id == models.Submenu.menu_id)
            .outerjoin(models.Dish, models.Submenu.id == models.Dish.submenu_id)
            .group_by(models.Menu.id)
        )

        menu = query.first()
        if not menu:
            raise HTTPException(
                detail='menu not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return menu

    def create(
            self,
            data: schemas.CreateMenu
    ) -> tuple[models.Menu, int, int]:
        stmt = insert(models.Menu).values(
            **data.model_dump(),
            id=uuid.uuid4()
        ).returning(models.Menu.id)

        menu = self.session.execute(stmt)
        self.session.commit()

        return self.get(id=menu.scalar_one())

    def patch(
            self,
            menu_id: uuid.UUID,
            data: schemas.UpdateMenu
    ) -> tuple[models.Menu, int, int]:
        menu_tuple = self.get(id=menu_id)
        for field, value in data:
            setattr(menu_tuple[0], field, value)

        self.session.commit()
        self.session.refresh(menu_tuple[0])

        return menu_tuple

    def delete(
            self,
            menu_id: uuid.UUID
    ) -> None:
        stmt = delete(models.Menu).where(
            models.Menu.id == menu_id
        )
        self.session.execute(stmt)
        self.session.commit()
