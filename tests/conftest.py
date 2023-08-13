import asyncio
import os

import pytest
from httpx import AsyncClient

app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')
api_version = '/api/v1/'

# BASE_URL = f"http://{app_host}:{app_port}{api_version}"
BASE_URL = 'http://127.0.0.1:8000/api/v1'


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def client():
    async with AsyncClient(base_url=BASE_URL) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def global_menu_data():
    data = {
        'id': '',
        'title': '',
        'description': '',
        'submenus_count': 0,
        'dishes_count': 0
    }
    return data


@pytest.fixture(scope='session', autouse=True)
def global_submenu_data():
    data = {
        'id': '',
        'title': '',
        'description': '',
        'menu_id': '',
        'dishes_count': 0
    }
    return data


@pytest.fixture(scope='session', autouse=True)
def global_dish_data():
    data = {
        'id': '',
        'title': '',
        'description': '',
        'submenu_id': '',
    }
    return data


@pytest.fixture(scope='module')
async def create_menu(
        client: AsyncClient,
        global_menu_data,
        global_submenu_data
):
    response = await client.post('/menus', json=global_menu_data)

    global_menu_data.update(response.json())
    global_submenu_data.update({'menu_id': response.json()['id']})

    assert response.status_code == 201

    yield

    response = await client.delete(f"/menus/{global_menu_data['id']}")
    assert response.status_code == 200


@pytest.fixture(scope='module')
async def create_menu_submenu(
        client: AsyncClient,
        create_menu,
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

    global_dish_data.update(
        {'submenu_id': response.json()['id']}
    )

    yield
