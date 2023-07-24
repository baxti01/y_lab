import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from src.dish.schemas import UpdateDish, Dish, CreateDish
from src.dish.service import DishService

router = APIRouter(
    tags=["Dish"]
)


@router.get(
    "/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[Dish]
)
def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        service: DishService = Depends()
):
    return service.get_dishes(submenu_id)


@router.get(
    "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Dish
)
def get_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    return service.get_dish(submenu_id, dish_id)


@router.post(
    "/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=Dish,
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: CreateDish,
        service: DishService = Depends()
):
    return service.create_dish(submenu_id, data)


@router.patch(
    "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Dish
)
def patch_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        data: UpdateDish,
        service: DishService = Depends()
):
    return service.patch_dish(submenu_id, dish_id, data)


@router.delete(
    "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
)
def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    service.delete_dish(submenu_id, dish_id)
    return {}
