import asyncio

from loguru import logger
from fastapi import HTTPException

from backend.api_v1.users.schemas import CreateUserSchema
from backend.config import settings
from backend.config.db import db_setup
from backend.api_v1.users.crud import create_user


superuser_schema = CreateUserSchema(
    login=settings.ADMIN_LOGIN,
    name='admin',
    surname='admin',
    active=True,
    salary=1,
    position_id=None,
    password_1=settings.ADMIN_PASSWORD,
    password_2=settings.ADMIN_PASSWORD,
)

async def create_superuser(session):
    try:
        superuser = await create_user(
            user_schema=superuser_schema,
            photo='',
            session=session,
            accountant=False,
            admin=True,
        )
        logger.info(f'Created super user {superuser.login}')
        return superuser
    except HTTPException:
        logger.info(f'This super user is already exists')
    finally:
        await session.aclose()


session = db_setup.session()


if __name__ == '__main__':
    asyncio.run(create_superuser(session))
