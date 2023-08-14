import pytest

uuidMenu = ''
uuidSubmenu = ''


@pytest.mark.asyncio
async def test_create_menu(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/', json={
        'title': 'menu 1',
        'description': 'menu 1 description'
    })
    assert response.status_code == 201
    global uuidMenu
    uuidMenu = response.json()['id']


@pytest.mark.asyncio
async def test_create_submenu(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus', json={
        'title': 'submenu 1',
        'description': 'submenu description 1'
    })
    assert response.status_code == 201
    global uuidSubmenu
    uuidSubmenu = response.json()['id']


@pytest.mark.asyncio
async def test_create_dish_1(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes',
                                 json={
                                     'title': 'dish 1',
                                     'description': 'dish 1 description',
                                     'price': '10.10'
                                 })
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_dish_2(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes',
                                 json={
                                     'title': 'dish 2',
                                     'description': 'dish 2 description',
                                     'price': '20.20'
                                 })
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_menu_1(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2


@pytest.mark.asyncio
async def test_get_submenu_1(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}')
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2


@pytest.mark.asyncio
async def test_delete_submenu(client, host):
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_submenus(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_dishes(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_menu_2(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


@pytest.mark.asyncio
async def test_delete_menu(client, host):
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_menus(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []
