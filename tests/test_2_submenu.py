import uuid

import pytest
from httpx import AsyncClient


@pytest.fixture(scope='module', autouse=True)
def create_menus(create_menu):
    pass


async def test_get_submenu_list(
        client: AsyncClient,
        global_submenu_data,
):
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus"
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_get_submenu(
        client: AsyncClient,
        global_submenu_data
):
    submenu_id = uuid.uuid4()
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{submenu_id}"
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


async def test_create_submenu(
        client: AsyncClient,
        global_submenu_data
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


async def test_update_submenu(
        client: AsyncClient,
        global_submenu_data
):
    global_submenu_data['title'] = 'Submenu title updated'
    global_submenu_data['description'] = 'Submenu description updated'
    response = await client.patch(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{global_submenu_data['id']}",
        json=global_submenu_data
    )

    assert response.status_code == 200
    assert response.json() == global_submenu_data


async def test_get_submenus(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus"
    )

    assert response.status_code == 200
    assert response.json() == [global_submenu_data]


async def test_get_submenu_by_id(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.get(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{global_submenu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json() == global_submenu_data


async def test_delete_submenu(
        client: AsyncClient,
        global_submenu_data
):
    response = await client.delete(
        f"/menus/{global_submenu_data['menu_id']}/submenus/{global_submenu_data['id']}"
    )

    assert response.status_code == 200
    assert response.json() == {}
