import uuid

from fastapi import APIRouter, Depends, status

from src.submenu.schemas import CreateSubmenu, Submenu, UpdateSubmenu
from src.submenu.service import SubmenuService

router = APIRouter(
    tags=['Submenu']
)


@router.get(
    '/menus/{menu_id}/submenus',
    response_model=list[Submenu]
)
def get_submenus(
        menu_id: uuid.UUID,
        service: SubmenuService = Depends()
):
    return service.get_submenus(menu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu
)
def get_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        service: SubmenuService = Depends()
):
    return service.get_submenu(menu_id, submenu_id)


@router.post(
    '/menus/{menu_id}/submenus',
    response_model=Submenu,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(
        menu_id: uuid.UUID,
        data: CreateSubmenu,
        service: SubmenuService = Depends()
):
    return service.create_submenu(menu_id, data)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu
)
def patch_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: UpdateSubmenu,
        service: SubmenuService = Depends()
):
    return service.patch_submenu(
        menu_id,
        submenu_id,
        data
    )


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        service: SubmenuService = Depends()
):
    service.delete_submenu(menu_id, submenu_id)
    return {}
