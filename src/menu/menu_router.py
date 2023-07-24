import uuid
from typing import List

from fastapi import APIRouter, Depends, Response, status

from src.menu.schemas import FullMenu, UpdateMenu, Menu, CreateMenu
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


@router.get("/{menu_id}", response_model=Menu)
def get_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    return service.get_menu(menu_id)


@router.post(
    "/",
    response_model=Menu,
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        data: CreateMenu,
        service: MenuService = Depends()
):
    return service.create_menu(data)


@router.patch("/{menu_id}", response_model=Menu)
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
