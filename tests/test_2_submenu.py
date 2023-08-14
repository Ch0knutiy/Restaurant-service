import pytest

uuidMenu = ''
uuid = ''
menuTitle = 'menu 1'
menuDescription = 'menu description 1'
submenuTitle = 'submenu 1'
submenuDescription = 'submenu description 1'
submenuTitleUpdate = 'new submenu 1'
submenuDescriptionUpdate = 'new submenu description 1'


@pytest.mark.asyncio
async def test_get_submenus(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/', json={
        'title': menuTitle,
        'description': menuDescription
    })
    assert response.status_code == 201
    global uuidMenu
    uuidMenu = response.json()['id']
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_submenu(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus', json={
        'title': submenuTitle,
        'description': submenuDescription
    })
    assert response.status_code == 201
    assert response.json()['title'] == submenuTitle
    assert response.json()['description'] == submenuDescription
    global uuid
    uuid = response.json()['id']
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_submenu(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitle
    assert response.json()['description'] == submenuDescription


@pytest.mark.asyncio
async def test_update_submenu(client, host):
    response = await client.patch(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuid}', json={
        'title': submenuTitleUpdate,
        'description': submenuDescriptionUpdate
    })
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitleUpdate
    assert response.json()['description'] == submenuDescriptionUpdate
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == submenuTitleUpdate
    assert response.json()['description'] == submenuDescriptionUpdate


@pytest.mark.asyncio
async def test_delete_submenu(client, host):
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuid}')
    assert response.status_code == 200
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus')
    assert response.status_code == 200
    assert response.json() == []
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuidMenu}/submenus/{uuid}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuidMenu}')
    assert response.status_code == 200
