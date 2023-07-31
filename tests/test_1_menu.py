import uuid

import pytest
from httpx import Client

pytest.menu_id = ""

MENU_ID: uuid.UUID


def test_get_menu_list(
        client: Client
):
    response = client.get("/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu(
        client: Client
):
    menu_id = uuid.uuid4()
    response = client.get(f"/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


def test_create_menu(
        client: Client,
        global_menu_data
):
    data = {
        "title": "Menu title",
        "description": "Menu description"
    }
    response = client.post("/menus", json=data)

    assert response.status_code == 201

    res_data = response.json()
    assert res_data
    assert res_data["title"] == data["title"]
    assert res_data["description"] == data["description"]

    global_menu_data.update(res_data)


def test_update_menu(
        client: Client,
        global_menu_data
):
    global_menu_data["title"] = "Menu title updated"
    global_menu_data["description"] = "Menu description updated"
    response = client.patch(
        f"/menus/{global_menu_data['id']}",
        json=global_menu_data
    )

    assert response.status_code == 200
    assert response.json() == global_menu_data


def test_get_menus(
        client: Client,
        global_menu_data
):
    response = client.get("/menus")
    assert response.status_code == 200
    assert response.json() == [global_menu_data]


def test_get_menu_by_id(
        client: Client,
        global_menu_data
):
    response = client.get(f"/menus/{global_menu_data['id']}")
    assert response.status_code == 200
    assert response.json() == global_menu_data


def test_delete_menu(
        client: Client,
        global_menu_data
):
    response = client.delete(f"/menus/{global_menu_data['id']}")

    assert response.status_code == 200
    assert response.json() == {}
