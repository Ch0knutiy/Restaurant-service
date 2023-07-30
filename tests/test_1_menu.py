import httpx

client = httpx.Client()
uuid = ""
menuTitle = "menu 1"
menuDescription = "menu description 1"
menuTitleUpdate = "new menu 1"
menuDescriptionUpdate = "new menu description 1"


def test_get_menus():
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu():
    response = client.post("http://fastapi_ylab:8000/api/v1/menus/", json={
            "title": menuTitle,
            "description": menuDescription
    })
    assert response.status_code == 201
    assert response.json()['title'] == menuTitle
    assert response.json()['description'] == menuDescription
    global uuid
    uuid = response.json()['id']
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/")
    assert response.status_code == 200
    assert response.json() != []


def test_get_menu():
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/" + uuid)
    assert response.status_code == 200
    assert response.json()['title'] == menuTitle
    assert response.json()['description'] == menuDescription


def test_update_menu():
    response = client.patch("http://fastapi_ylab:8000/api/v1/menus/" + uuid, json={
        "title": menuTitleUpdate,
        "description": menuDescriptionUpdate
    })
    assert response.status_code == 200
    assert response.json()['title'] == menuTitleUpdate
    assert response.json()['description'] == menuDescriptionUpdate
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/" + uuid)
    assert response.status_code == 200
    assert response.json()['title'] == menuTitleUpdate
    assert response.json()['description'] == menuDescriptionUpdate


def test_delete_menu():
    response = client.delete("http://fastapi_ylab:8000/api/v1/menus/" + uuid)
    assert response.status_code == 200
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/")
    assert response.status_code == 200
    assert response.json() == []
    response = client.get("http://fastapi_ylab:8000/api/v1/menus/" + uuid)
    assert response.status_code == 404
    assert response.json()['detail'] == "menu not found"
