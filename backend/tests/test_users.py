import json
import random
import pytest

from loguru import logger

from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_list_user_admin(client: AsyncClient,
                                admin,
                                ):
    response = await client.get(
        'users/get/list',
        headers={'Authorization': admin,
                     'Content-Type': 'application/json',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_create_update_delete_user(client: AsyncClient,
                                        payload_create_user_accountant,
                                        admin,
                                        ):
    response = await client.put(
        'users/create',
        data=dict(user_schema=json.dumps(payload_create_user_accountant), photo=''),
        headers={'Authorization': admin,
                 'Accept': '*/*',
                 },
        )
    dict_res = response.json()
    logger.info(f'response {response.content}')
    assert response.status_code == 201
    assert response.json() == {'active': True,
                               'country_code': 'RU',
                               'create_date': dict_res['create_date'],
                               'id': dict_res['id'],
                               'login': dict_res['login'],
                               'login_date': None,
                               'middle_name': None,
                               'name': 'random',
                               'phone_number': '9006001000',
                               'picture': None,
                               'position_id': 1,
                               'surname': 'random',
                               }

    login = str(random.randint(10000000, 210003203231))
    data = dict(login=login,
                name='alex',
                )
    response = await client.patch(
        url=f'users/update/{dict_res["id"]}',
        data=dict(user_schema=json.dumps(data), photo=''),
        headers={'Authorization': admin,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 200
    assert response.json()['login'] == login
    assert response.json()['name'] == 'alex'

    response = await client.delete(
        url=f'/users/delete/{dict_res["id"]}',
        headers={'Authorization': admin,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 204


@pytest.mark.asyncio()
async def test_permission_create_update_delete_user(client: AsyncClient,
                                                    payload_create_user_accountant: dict,
                                                    user,
                                                    ):
    response = await client.put(
        'users/create',
        data=dict(user_schema=json.dumps(payload_create_user_accountant), photo=''),
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
        )
    assert response.status_code == 403

    response = await client.patch(
        url=f'users/update/33',
        data=dict(user_schema=json.dumps({'login': 'some'}), photo=''),
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 403

    response = await client.delete(
        url=f'/users/delete/33',
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 403


@pytest.mark.asyncio()
async def test_get_list_users(client: AsyncClient,
                         user,
                         ):
    response = await client.get(
        url='users/get/list',
        headers={'Authorization': user,
                 'Accept': '*/*',
                 },
    )
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_create_user_duck(client: AsyncClient,
                                payload_create_user_accountant,
                                accountant,
                                ):
    payload = payload_create_user_accountant.copy()
    payload['position_id'] = None
    payload['login'] = 'some_login'
    response = await client.put(
        'users/create',
        data=dict(user_schema=json.dumps(payload), photo=''),
        headers={'Authorization': accountant,
                 'Accept': '*/*',
                 },
        )
    logger.info(f'status code {response.status_code}')
    logger.info(f'detail = {response.content}')
    assert response.status_code == 400
    assert response.json() == dict(detail=dict(position_id='Cant be null'))


@pytest.mark.asyncio()
async def test_create_accountant(client: AsyncClient,
                                payload_create_user_accountant,
                                admin,
                                ):
    payload_create_user_accountant['position_id'] = None
    payload_create_user_accountant['login'] = 'accountant2'
    response = await client.put(
        'users/create/accountant',
        data=dict(user_schema=json.dumps(
            payload_create_user_accountant,
            ), photo=''),
        headers={'Authorization': admin,
                 'Accept': '*/*',
                 },
        )
    logger.info(f'status code {response.status_code}')
    logger.info(f'detail = {response.content}')
    assert response.status_code == 201


@pytest.mark.asyncio()
async def test_cancel_permission_create_accountant(client: AsyncClient,
                                                    payload_create_user_accountant,
                                                    accountant,
                                                    ):
    payload_create_user_accountant['position_id'] = None
    payload_create_user_accountant['login'] = 'accountant3'
    response = await client.put(
        'users/create/accountant',
        data=dict(user_schema=json.dumps(
            payload_create_user_accountant,
            ), photo=''),
        headers={'Authorization': accountant,
                 'Accept': '*/*',
                 },
        )
    logger.info(f'status code {response.status_code}')
    logger.info(f'detail = {response.content}')

    assert response.status_code == 403
    assert response.json() == dict(detail='Permission denied')
