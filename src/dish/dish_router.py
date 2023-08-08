import uuid

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from src.dish.schemas import CreateDish, Dish, UpdateDish
from src.dish.service import DishService

router = APIRouter(
    tags=['Dish']
)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[Dish]
)
@cache(expire=300)
def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        service: DishService = Depends()
):
    return service.get_dishes(menu_id, submenu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish
)
@cache(expire=300)
def get_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    return service.get_dish(menu_id, submenu_id, dish_id)


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=Dish,
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: CreateDish,
        service: DishService = Depends()
):
    return service.create_dish(menu_id, submenu_id, data)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish
)
def patch_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        data: UpdateDish,
        service: DishService = Depends()
):
    return service.patch_dish(menu_id, submenu_id, dish_id, data)


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
)
def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    service.delete_dish(menu_id, submenu_id, dish_id)
    return {}
