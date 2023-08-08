import uuid

from fastapi import APIRouter, Depends, status

from src.menu.schemas import CreateMenu, Menu, UpdateMenu
from src.menu.service import MenuService

router = APIRouter(
    tags=['Menu']
)


@router.get('/menus', response_model=list[Menu])
def get_menus(
        service: MenuService = Depends()
):
    return service.get_menus()


@router.get('/menus/{menu_id}', response_model=Menu)
def get_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    return service.get_menu(menu_id)


@router.post(
    '/menus',
    response_model=Menu,
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        data: CreateMenu,
        service: MenuService = Depends()
):
    return service.create_menu(data)


@router.patch('/menus/{menu_id}', response_model=Menu)
def patch_menu(
        menu_id: uuid.UUID,
        data: UpdateMenu,
        service: MenuService = Depends()
):
    return service.patch_menu(menu_id, data)


@router.delete(
    '/menus/{menu_id}',
)
def delete_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    service.delete_menu(menu_id)
    return {}
