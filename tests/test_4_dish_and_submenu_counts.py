import httpx

client = httpx.Client()
uuidMenu = ''
uuidSubmenu = ''


def test_create_menu():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/', json={
        'title': 'menu 1',
        'description': 'menu 1 description'
    })
    assert response.status_code == 201
    global uuidMenu
    uuidMenu = response.json()['id']


def test_create_submenu():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus', json={
        'title': 'submenu 1',
        'description': 'submenu description 1'
    })
    assert response.status_code == 201
    global uuidSubmenu
    uuidSubmenu = response.json()['id']


def test_create_dish_1():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuidSubmenu + '/dishes',
                           json={
                               'title': 'dish 1',
                               'description': 'dish 1 description',
                               'price': '10.10'
                           })
    assert response.status_code == 201


def test_create_dish_2():
    response = client.post('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuidSubmenu + '/dishes',
                           json={
                               'title': 'dish 2',
                               'description': 'dish 2 description',
                               'price': '20.20'
                           })
    assert response.status_code == 201


def test_get_menu_1():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu)
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2


def test_get_submenu_1():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuidSubmenu)
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2


def test_delete_submenu():
    response = client.delete('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuidSubmenu)
    assert response.status_code == 200


def test_get_submenus():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus')
    assert response.status_code == 200
    assert response.json() == []


def test_get_dishes():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu + '/submenus/' + uuidSubmenu + '/dishes')
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu_2():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu)
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_delete_menu():
    response = client.delete('http://fastapi_ylab:8000/api/v1/menus/' + uuidMenu)
    assert response.status_code == 200


def test_get_menus():
    response = client.get('http://fastapi_ylab:8000/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []
