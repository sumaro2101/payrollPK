from typing import Annotated

from datetime import datetime

from jwt import InvalidTokenError
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from loguru import logger

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordBearer

from backend.api_v1.auth.utils import check_type_token, decode_jwt
from backend.config import settings
from backend.config.db import db_setup
from backend.config.models.user import User
from .exeptions import raise_incorect_values, raise_non_active_user, InvalidAlgorithm
from backend.hashers.hasher_password import PasswordHashCheker


security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


@logger.catch(reraise=True, exclude=HTTPException)
async def get_authenticate(
    form_data: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession,
    ):
    login = form_data.username
    password = form_data.password
    logger.debug(f'try login {login}')
    stmt = (Select(User)
            .where(User.login == login)
            .options(selectinload(User.position)))
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


async def get_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=dict(token='Не правильный токен'),
                            )
    return payload
  
    
async def get_current_active_user(payload: dict = Depends(get_payload),
                                  session: AsyncSession = Depends(db_setup.get_session),
                                  ):
    token_type = payload.get(settings.AUTH_JWT.TOKEN_TYPE_FIELD)
    check_type_token(token_type, settings.AUTH_JWT.ACCESS_TOKEN_TYPE)
    username = payload.get('username')
    stmt = (Select(User)
            .where(User.login == username)
            .options(selectinload(User.position)))
    user = await session.scalar(stmt)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=dict(user='Токен не верный'),
                            )

    return user
