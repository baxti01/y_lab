import uuid
from typing import List

from fastapi import APIRouter, Depends, Response, status

from src.menu.schemas import FullMenu, BaseMenu, UpdateMenu
from src.menu.service import MenuService

router = APIRouter(
    prefix="/menus",
    tags=["Menu"]
)


@router.get('/', response_model=List[FullMenu])
def get_menus(
        service: MenuService = Depends()
):
    return service.get_menus()


@router.get("/{menu_id}", response_model=BaseMenu)
def get_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    return service.get_menu(menu_id)


@router.post(
    "/",
    response_model=BaseMenu,
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        data: BaseMenu,
        service: MenuService = Depends()
):
    return service.create_menu(data)


@router.patch("/{menu_id}", response_model=BaseMenu)
def patch_menu(
        menu_id: uuid.UUID,
        data: UpdateMenu,
        service: MenuService = Depends()
):
    return service.patch_menu(menu_id, data)


@router.delete(
    "/{menu_id}",
)
def delete_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    service.delete_menu(menu_id)
    return {}
