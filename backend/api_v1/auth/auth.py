from typing import Annotated

from datetime import datetime

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.config.db import db_setup
from backend.config.models.user import User
from .exeptions import raise_incorect_values, raise_non_active_user
from backend.hashers.hasher_password import PasswordHashCheker


security = HTTPBasic()


async def get_active_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(db_setup.get_session),
    ):
    login = credentials.username
    password = credentials.password

    stmt = (Select(User)
            .where(User.login == login))
    user: User = await session.scalar(statement=stmt)
    if not user:
        raise_incorect_values()
    some_password = PasswordHashCheker(password=password,
                                       hash_password=user.password,
                                       ).is_correct()
    if not some_password:
        raise_incorect_values()

    if not user.active:
        raise_non_active_user()
    user.login_date = datetime.now()
    await session.commit()

    return user
