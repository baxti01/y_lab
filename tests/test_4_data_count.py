import pytest
from httpx import AsyncClient


async def test_create_menu(
        client: AsyncClient,
        global_menu_data,
        global_submenu_data
):
    data = {
        'title': 'Menu title',
        'description': 'Menu description'
    }
    response = await client.post('/menus', json=data)

    assert response.status_code == 201

    res_data = response.json()
    assert res_data
    assert res_data['title'] == data['title']
    assert res_data['description'] == data['description']

    global_menu_data.update(res_data)
    global_submenu_data.update({'menu_id': res_data['id']})


async def test_create_submenu(
        client: AsyncClient,
        global_submenu_data,
        global_dish_data
):
    data = {
        'title': 'Submenu title',
        'description': 'Submenu description'
    }
    response = await client.post(
        f"/menus/{global_submenu_data['menu_id']}/submenus",
        json=data
    )
    assert response.status_code == 201

    res_data = response.json()
    assert res_data
    assert res_data['title'] == data['title']
    assert res_data['description'] == data['description']

    global_submenu_data.update(res_data)
    global_dish_data.update({'submenu_id': res_data['id']})


@pytest.mark.parametrize(
    'data',
    [
        {
            'title': 'Dish 1 title',
            'description': 'Dish 1 description',
            'price': '1.00'
        },
        {
            'title': 'Dish 2 title',
            'description': 'Dish 2 description',
            'price': '2.00'
        }
    ]
)
async def test_create_dishes(
        client: AsyncClient,
        global_menu_data,
        global_dish_data,
        data,
):
    response = await client.post(
        f"/menus/{global_menu_data['id']}"
        f"/submenus/{global_dish_data['submenu_id']}"
        f'/dishes',
        json=data
    )

    assert response.status_code == 201

    res_data = response.json()

    assert res_data['title'] == data['title']
    assert res_data['description'] == data['description']
    assert res_data['price'] == data['price']

    global_dish_data.update(response.json())


async def test_get_menu(
        client: AsyncClient,
        global_menu_data
):
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2


async def test_get_submenu(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{global_submenu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2


async def test_delete_submenu(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.delete(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{global_submenu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json() == {}


async def test_get_submenus(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus"
    )

    assert response.status_code == 200
    assert response.json() == []


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
    assert response.json() == []


async def test_get_menu_2(
        client: AsyncClient,
        global_menu_data
):
    response = await client.get(
        f"/menus/{global_menu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


async def test_delete_menu(
        client: AsyncClient,
        global_menu_data
):
    response = await client.delete(f"/menus/{global_menu_data['id']}")

    assert response.status_code == 200
    assert response.json() == {}


async def test_get_menus(
        client: AsyncClient,
        global_menu_data
):
    response = await client.get('/menus')
    assert response.status_code == 200
    assert response.json() == []
