from sqlalchemy import Select, ScalarResult, Insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from sqlalchemy_utils import PhoneNumber
from sqlalchemy_imageattach.context import store_context

from fastapi import UploadFile, status, HTTPException

from backend.config.models import User
from backend.hashers import PasswordHasher
from backend.handlers.handle_error import sql_parse_error_message
from .schemas import CreateUserSchema
from .passwords import PasswordsChecker
from loguru import logger


async def get_users(session: AsyncSession):
    stmt = (Select(User)
            .options(selectinload(User.position))
            .order_by(User.id))
    users: ScalarResult[User] = await session.scalars(statement=stmt)
    return list(users)

async def create_user(user_schema: CreateUserSchema,
                      photo: UploadFile,
                      session: AsyncSession,
                      ) -> User:
    password_1, password_2 = user_schema.password_1, user_schema.password_2
    checked_password = PasswordsChecker(
        password_1=password_1,
        password_2=password_2,
        ).get_password()
    hashed_password = PasswordHasher(password=checked_password).get_hashed_password()
    phone_number = PhoneNumber(user_schema.phone_number, user_schema.country_code)
    logger.info(f'user_schema = {user_schema}')
    preform_create = (User(**user_schema.model_dump(exclude=('password_1',
                                                             'password_2',
                                                             'phone_number',
                                                             'county_code',
                                                             )),
                           password=hashed_password,
                           phone=phone_number,
                           ))
    try:
        session.add(preform_create)
        await session.commit()
        await session.refresh(preform_create)
    except IntegrityError as ex:
        error = sql_parse_error_message(ex=ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(user=error))
    return user_schema
