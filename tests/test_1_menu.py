import uuid

from httpx import AsyncClient


async def test_get_menu_list(
        client: AsyncClient
):
    response = await client.get('/menus')
    assert response.status_code == 200
    assert response.json() == []


async def test_get_menu(
        client: AsyncClient
):
    menu_id = uuid.uuid4()
    response = await client.get(f'/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


async def test_create_menu(
        client: AsyncClient,
        global_menu_data
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


async def test_update_menu(
        client: AsyncClient,
        global_menu_data
):
    global_menu_data['title'] = 'Menu title updated'
    global_menu_data['description'] = 'Menu description updated'
    response = await client.patch(
        f"/menus/{global_menu_data['id']}",
        json=global_menu_data
    )

    assert response.status_code == 200
    assert response.json() == global_menu_data


async def test_get_menus(
        client: AsyncClient,
        global_menu_data
):
    response = await client.get('/menus')
    assert response.status_code == 200
    assert response.json() == [global_menu_data]


async def test_get_menu_by_id(
        client: AsyncClient,
        global_menu_data
):
    response = await client.get(f"/menus/{global_menu_data['id']}")
    assert response.status_code == 200
    assert response.json() == global_menu_data


async def test_delete_menu(
        client: AsyncClient,
        global_menu_data
):
    response = await client.delete(f"/menus/{global_menu_data['id']}")

    assert response.status_code == 200
    assert response.json() == {}
