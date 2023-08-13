import uuid

import pytest
from httpx import AsyncClient


@pytest.fixture(scope='module', autouse=True)
async def create_menu_and_submenu(create_menu_submenu):
    pass


async def test_get_dish_list(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f'/dishes'
    )

    assert response.status_code == 200
    assert response.json() == []


async def test_get_dish(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    dish_id = uuid.uuid4()
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f'/dishes/{dish_id}'
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


async def test_create_dish(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    data = {
        'title': 'Dish title',
        'description': 'Dish description',
        'price': '0.00'
    }

    response = await client.post(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f'/dishes',
        json=data
    )

    assert response.status_code == 201
    assert response.json()
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']
    assert response.json()['price'] == data['price']

    global_dish_data.update(response.json())


async def test_update_dish(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    global_dish_data['title'] = 'Dish title updated'
    global_dish_data['description'] = 'Dish description updated'
    global_dish_data['price'] = '5.00'

    response = await client.patch(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f"/dishes/{global_dish_data['id']}",
        json=global_dish_data
    )

    assert response.status_code == 200
    assert response.json() == global_dish_data


async def test_get_dishes(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f'/dishes'
    )

    assert response.status_code == 200
    assert response.json() == [global_dish_data]


async def test_get_dish_by_id(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f"/dishes/{global_dish_data['id']}"
    )

    assert response.status_code == 200
    assert response.json() == global_dish_data


async def test_delete_dish(
        client: AsyncClient,
        global_dish_data,
        global_menu_data
):
    response = await client.delete(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f"/dishes/{global_dish_data['id']}"
    )

    assert response.status_code == 200
    assert response.json() == {}
