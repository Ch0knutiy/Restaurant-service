import pytest

uuidMenu = ''
uuidSubmenu = ''
uuid = ''
menuTitle = 'menu 1'
menuDescription = 'menu description 1'
submenuTitle = 'submenu 1'
submenuDescription = 'submenu description 1'
dishTitle = 'dish 1'
dishDescription = 'dish description'
dishPrice = '10.10'
dishTitleUpdate = 'new dish 1'
dishDescriptionUpdate = 'new dish description 1'
dishPriceUpdate = '20.20'


@pytest.mark.asyncio
async def test_get_dishes(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/', json={
        'title': menuTitle,
        'description': menuDescription
    })
    assert response.status_code == 201
    global uuidMenu, uuidSubmenu
    uuidMenu = response.json()['id']
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus', json={
        'title': submenuTitle,
        'description': submenuDescription
    })
    assert response.status_code == 201
    uuidSubmenu = response.json()['id']
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_dish(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes',
                                 json={
                                     'title': dishTitle,
                                     'description': dishDescription,
                                     'price': dishPrice
                                 })
    assert response.status_code == 201
    assert response.json()['title'] == dishTitle
    assert response.json()['description'] == dishDescription
    assert response.json()['price'] == dishPrice
    global uuid
    uuid = response.json()['id']
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes')
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_dish(client, host):
    response = await client.get(
        f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == dishTitle
    assert response.json()['description'] == dishDescription
    assert response.json()['price'] == dishPrice


@pytest.mark.asyncio
async def test_update_dish(client, host):
    response = await client.patch(
        f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes/{uuid}',
        json={'title': dishTitleUpdate,
              'description': dishDescriptionUpdate,
              'price': dishPriceUpdate
              })
    assert response.status_code == 200
    assert response.json()['title'] == dishTitleUpdate
    assert response.json()['description'] == dishDescriptionUpdate
    assert response.json()['price'] == dishPriceUpdate
    response = await client.get(
        f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == dishTitleUpdate
    assert response.json()['description'] == dishDescriptionUpdate
    assert response.json()['price'] == dishPriceUpdate


@pytest.mark.asyncio
async def test_delete_dish(client, host):
    response = await client.delete(
        f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes/{uuid}')
    assert response.status_code == 200
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes')
    assert response.status_code == 200
    assert response.json() == []
    response = await client.get(
        f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}/dishes/{uuid}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuidSubmenu}')
    assert response.status_code == 200
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}')
    assert response.status_code == 200
