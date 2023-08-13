import uuid

from fastapi import APIRouter, Depends, status

from src.dish.schemas import CreateDish, Dish, UpdateDish
from src.dish.service import DishService

router = APIRouter(
    tags=['Dish']
)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[Dish]
)
async def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        service: DishService = Depends()
):
    data = await service.get_dishes(menu_id, submenu_id)
    print('API da', data)
    return data


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish
)
async def get_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    return await service.get_dish(menu_id, submenu_id, dish_id)


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=Dish,
    status_code=status.HTTP_201_CREATED
)
async def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: CreateDish,
        service: DishService = Depends()
):
    return await service.create_dish(menu_id, submenu_id, data)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish
)
async def patch_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        data: UpdateDish,
        service: DishService = Depends()
):
    return await service.patch_dish(menu_id, submenu_id, dish_id, data)


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
)
async def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        service: DishService = Depends()
):
    await service.delete_dish(menu_id, submenu_id, dish_id)
    return {}
