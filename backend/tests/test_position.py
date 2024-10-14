from httpx import AsyncClient
import pytest
import json

from loguru import logger


@pytest.mark.asyncio
async def testcreate_update_delete_position(client: AsyncClient,
                                            accountant,
                                            ):
    response = await client.put(
        url='positions/create',
        json=dict(name='position'),
        headers={'Authorization': accountant,
                 'Accept': '*/*',
                 },
    )
    res = response.json()
    logger.info(f'responce = {res}')
    assert response.status_code == 201
    assert res['name'] == 'position'

    response = await client.patch(
        url=f'positions/update/{res["id"]}',
        json=dict(name='new_position'),
        headers={'Authorization': accountant,
                 'Accept': '*/*',
                 },
    )
    res = response.json()
    logger.info(f'responce = {res}')
    assert response.status_code == 200
    assert res['name'] == 'new_position'

    response = await client.delete(
        url=f'positions/delete/{res["id"]}',
        headers={'Authorization': accountant,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_cancel_permissions_user_position(client: AsyncClient,
                                                user,
                                                ):
    response = await client.put(
        url='positions/create',
        json=dict(name='position'),
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    res = response.json()
    logger.info(f'responce = {res}')
    assert response.status_code == 403

    response = await client.patch(
        url=f'positions/update/33',
        json=dict(name='new_position'),
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    res = response.json()
    logger.info(f'responce = {res}')
    assert response.status_code == 403

    response = await client.delete(
        url=f'positions/delete/33',
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 403
