import os

import pytest
from httpx import Client

app_host = os.environ.get("APP_HOST")
app_port = os.environ.get("APP_PORT")
api_version = "/api/v1/"

BASE_URL = f"http://{app_host}:{app_port}{api_version}"


@pytest.fixture(scope="session", autouse=True)
def client():
    client = Client(base_url=BASE_URL)
    return client


@pytest.fixture(scope="session", autouse=True)
def global_menu_data():
    data = {
        "id": "",
        "title": "",
        "description": "",
        "submenus_count": 0,
        "dishes_count": 0
    }
    return data


@pytest.fixture(scope="session", autouse=True)
def global_submenu_data():
    data = {
        "id": "",
        "title": "",
        "description": "",
        "menu_id": "",
        "dishes_count": 0
    }
    return data


@pytest.fixture(scope="session", autouse=True)
def global_dish_data():
    data = {
        "id": "",
        "title": "",
        "description": "",
        "submenu_id": "",
    }
    return data


@pytest.fixture(scope="module")
def create_menu(
        client: Client,
        global_menu_data,
        global_submenu_data
):
    response = client.post("/menus", json=global_menu_data)

    global_menu_data.update(response.json())
    global_submenu_data.update({"menu_id": response.json()['id']})

    assert response.status_code == 201

    yield

    response = client.delete(f"/menus/{global_menu_data['id']}")
    assert response.status_code == 200


@pytest.fixture(scope="module")
def create_menu_submenu(
        client: Client,
        create_menu,
        global_submenu_data,
        global_dish_data
):
    data = {
        "title": "Submenu title",
        "description": "Submenu description"
    }
    response = client.post(
        f"/menus/{global_submenu_data['menu_id']}/submenus",
        json=data
    )
    assert response.status_code == 201

    global_dish_data.update(
        {"submenu_id": response.json()["id"]}
    )

    yield
