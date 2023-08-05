import httpx

client = httpx.Client()
uuidMenu = ''
uuid = ''
menuTitle = 'menu 1'
menuDescription = 'menu description 1'
submenuTitle = 'submenu 1'
submenuDescription = 'submenu description 1'
submenuTitleUpdate = 'new submenu 1'
submenuDescriptionUpdate = 'new submenu description 1'


def test_get_submenus():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/', json={
        'title': menuTitle,
        'description': menuDescription
    })
    assert response.status_code == 201
    global uuidMenu
    uuidMenu = response.json()['id']
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus')
    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus', json={
        'title': submenuTitle,
        'description': submenuDescription
    })
    assert response.status_code == 201
    assert response.json()['title'] == submenuTitle
    assert response.json()['description'] == submenuDescription
    global uuid
    uuid = response.json()['id']
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus')
    assert response.status_code == 200
    assert response.json() != []


def test_get_submenu():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuid)
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitle
    assert response.json()['description'] == submenuDescription


def test_update_submenu():
    response = client.patch('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuid, json={
        'title': submenuTitleUpdate,
        'description': submenuDescriptionUpdate
    })
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitleUpdate
    assert response.json()['description'] == submenuDescriptionUpdate
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuid)
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitleUpdate
    assert response.json()['description'] == submenuDescriptionUpdate


def test_delete_submenu():
    response = client.delete('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuid)
    assert response.status_code == 200
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus')
    assert response.status_code == 200
    assert response.json() == []
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuid)
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'
    response = client.delete('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu)
    assert response.status_code == 200
