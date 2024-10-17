import asyncio
from contextlib import asynccontextmanager
import httpx
import pytest_asyncio
import pytest
from asgi_lifespan import LifespanManager
import random
import base64

from fastapi import FastAPI

from sqlalchemy.pool import NullPool
import sys

from loguru import logger

from backend.config.db import db_test
from backend.config.db import db_setup as database
from backend.config.models import Base
from backend.api_v1.routers import router
from backend.config import settings
from backend.api_v1.users.superuser import create_superuser
from backend.config.models.position import Position
from backend.config.models.user import User
from backend.hashers import PasswordHasher
from backend.api_v1.auth.tokens import Token


db_setup = db_test(db_url=settings.DB.test_url,
                   poolclass_=NullPool,
                   )


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db_setup.engine.url = settings.DB.test_url
        logger.info(db_setup.engine.url)
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            sys.stdout.write('alembic upgrade head')
        yield
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    app.dependency_overrides[database.get_session] = override_get_async_session

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope='session')
async def client(app):
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000/api/v1/") as client:
        yield client


@pytest_asyncio.fixture(scope='session')
async def admin():
    async with db_setup.session() as session:
        user = await create_superuser(session)
    token = Token(user=user).create_access_token()
    token = f'Bearer {token}'
    return token


@pytest_asyncio.fixture(scope='session')
async def position():
    async with db_setup.session() as session:
        stmt = Position(name=f'test{random.randint(1, 210003)}')
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
    logger.info(f'Position = {stmt.id}')
    return stmt


@pytest.fixture(scope='session')
def payload_create_user_accountant(position):
    id = random.randint(1, 21000)
    password = random.randint(10000000, 21000320000)
    return {
        'id': id,
        'login': str(random.randint(10000000, 210003203231)),
        'name': 'random',
        'surname': 'random',
        'active': True,
        'salary': 1.00,
        'position_id': position.id,
        'password_1': str(password),
        'password_2': str(password),
    }


@pytest_asyncio.fixture(scope='session')
async def user(payload_create_user_accountant: dict):
    payload = payload_create_user_accountant.copy()
    payload.pop('password_1')
    payload.pop('password_2')
    password = PasswordHasher(
        password=payload_create_user_accountant['password_1'],
        ).get_hashed_password()
    payload.update(password=password,
                   login='user',
                   _phone_number='9006001000',
                   country_code='RU',
                   id=11111,
                   )
    async with db_setup.session() as session:
        user = User(**payload)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    token = Token(user=user).create_access_token()
    token = f'Bearer {token}'
    logger.info(f'Bearer token = {token}')
    return token


@pytest_asyncio.fixture(scope='session')
async def accountant(payload_create_user_accountant: dict):
    payload = payload_create_user_accountant.copy()
    payload['id'] = 44444
    payload['login'] = 'accountant'
    payload.pop('password_1')
    payload.pop('password_2')
    password = PasswordHasher(
        password=payload_create_user_accountant['password_1'],
        ).get_hashed_password()
    payload.update(password=password,
                   _phone_number='9006001000',
                   country_code='RU',
                   is_accountant=True,
                   )
    async with db_setup.session() as session:
        user = User(**payload)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    token = Token(user=user).create_access_token()
    token = f'Bearer {token}'
    return token
