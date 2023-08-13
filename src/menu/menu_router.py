import uuid

from fastapi import APIRouter, Depends, status

from src.menu.schemas import CreateMenu, Menu, UpdateMenu
from src.menu.service import MenuService

router = APIRouter(
    tags=['Menu']
)


@router.get('/menus', response_model=list[Menu])
async def get_menus(
        service: MenuService = Depends()
):
    return await service.get_menus()


@router.get('/menus/{menu_id}', response_model=Menu)
async def get_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    return await service.get_menu(menu_id)


@router.post(
    '/menus',
    response_model=Menu,
    status_code=status.HTTP_201_CREATED
)
async def create_menu(
        data: CreateMenu,
        service: MenuService = Depends()
):
    return await service.create_menu(data)


@router.patch('/menus/{menu_id}', response_model=Menu)
async def patch_menu(
        menu_id: uuid.UUID,
        data: UpdateMenu,
        service: MenuService = Depends()
):
    return await service.patch_menu(menu_id, data)


@router.delete(
    '/menus/{menu_id}',
)
async def delete_menu(
        menu_id: uuid.UUID,
        service: MenuService = Depends()
):
    await service.delete_menu(menu_id)
    return {}
