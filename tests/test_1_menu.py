import pytest

uuid = ''
menuTitle = 'menu 1'
menuDescription = 'menu description 1'
menuTitleUpdate = 'new menu 1'
menuDescriptionUpdate = 'new menu description 1'


@pytest.mark.asyncio
async def test_get_menus(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_menu(client, host):
    response = await client.post(f'http://{host}:8000/api/v1/menus/',
                                 json={
                                     'title': menuTitle,
                                     'description': menuDescription
                                 })
    assert response.status_code == 201
    assert response.json()['title'] == menuTitle
    assert response.json()['description'] == menuDescription
    global uuid
    uuid = response.json()['id']
    response = await client.get(f'http://{host}:8000/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_menu(client, host):
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == menuTitle
    assert response.json()['description'] == menuDescription


@pytest.mark.asyncio
async def test_update_menu(client, host):
    response = await client.patch(f'http://{host}:8000/api/v1/menus/{uuid}', json={
        'title': menuTitleUpdate,
        'description': menuDescriptionUpdate
    })
    assert response.status_code == 200
    assert response.json()['title'] == menuTitleUpdate
    assert response.json()['description'] == menuDescriptionUpdate
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == menuTitleUpdate
    assert response.json()['description'] == menuDescriptionUpdate


@pytest.mark.asyncio
async def test_delete_menu(client, host):
    response = await client.delete(f'http://{host}:8000/api/v1/menus/{uuid}')
    assert response.status_code == 200
    response = await client.get(f'http://{host}:8000/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []
    response = await client.get(f'http://{host}:8000/api/v1/menus/{uuid}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'
