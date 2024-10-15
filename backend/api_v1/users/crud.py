from sqlalchemy import Select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from sqlalchemy_utils import PhoneNumber

from fastapi import UploadFile, status, HTTPException

from sqlalchemy_utils import PhoneNumberParseException

from backend.config.models import User
from backend.hashers import PasswordHasher
from backend.handlers.handle_error import sql_parse_error_message
from .schemas import CreateUserSchema, UpdateUserSchema
from .passwords import PasswordsChecker
from .utils import (upload_file,
                    rename_dir_of_login,
                    rm_save_upload_file,
                    make_image_directory,
                    delete_dir,
                    )
from loguru import logger


@logger.catch(reraise=True, exclude=HTTPException)
async def get_users(user: User,
                    session: AsyncSession,
                    ):
    stmt = (Select(User)
            .options(selectinload(User.position))
            .order_by(User.id))
    users: ScalarResult[User] = await session.scalars(statement=stmt)
    result = list(users)
    if user.is_accountant or user.is_admin:
        return result
    else:
        for item in result:
            delattr(item, 'salary')
        return result


@logger.catch(reraise=True, exclude=(HTTPException, PhoneNumberParseException))
async def create_user(user_schema: CreateUserSchema,
                      photo: UploadFile,
                      session: AsyncSession,
                      accountant: bool,
                      admin: bool = False,
                      ) -> User:
    logger.debug(f'try create user {user_schema.model_dump(exclude=("password_1", "password_2"))}')
    logger.debug(f'photo {photo}')
    if not user_schema.position_id and not (admin or accountant):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(position_id='Cant be null'))
    password_1, password_2 = user_schema.password_1, user_schema.password_2
    checked_password = PasswordsChecker(
        password_1=password_1,
        password_2=password_2,
        ).get_password()
    hashed_password = PasswordHasher(
        password=checked_password,
        ).get_hashed_password()
    try:
        phone_number = PhoneNumber(
            user_schema.phone_number,
            user_schema.country_code,
            check_region=True,
            )
    except PhoneNumberParseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(phone_number='Invalid phone number'))
    logger.info(f'user_schema = {user_schema}')
    preform_create = (User(**user_schema.model_dump(exclude=(
        'password_1',
        'password_2',
        'phone_number',
        'county_code')),
                           password=hashed_password,
                           phone=phone_number,
                           is_accountant=accountant,
                           is_admin=admin
                           ))
    try:
        session.add(preform_create)
        await session.commit()
        await session.refresh(preform_create)
        make_image_directory(dir_name=preform_create.login)
        if photo:
            image_url = await upload_file(
                file=photo,
                login=preform_create.login,
            )
            preform_create.picture = image_url
            await session.commit()
    except IntegrityError as ex:
        error = sql_parse_error_message(ex=ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(user=error))
    logger.debug(
        f'has create user {preform_create.id} {preform_create.login}: {preform_create}',
        )
    return preform_create


@logger.catch(reraise=True, exclude=(HTTPException, PhoneNumberParseException))
async def update_user(user: User,
                      user_schema: UpdateUserSchema,
                      photo: UploadFile | str,
                      session: AsyncSession,
                      ):
    phone_number = False
    if 'country_code' in user_schema.model_dump() or phone_number in user_schema.model_dump():
        try:
            phone_number = PhoneNumber(
            user_schema.phone_number if user_schema.phone_number else user._phone_number,
            user_schema.country_code if user_schema.country_code else user.country_code,
            check_region=True,
            )
        except PhoneNumberParseException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(phone_number='Invalid phone number'))
    values = user_schema.model_dump(exclude_unset=True,
                                    exclude_none=True,
                                    exclude=('phone_number',
                                             'country_code',
                                             )
                                    )
    if phone_number:
        values.update(phone_number=phone_number)
    logger.debug(f'try change user {user.id} {user.login} {user}')
    logger.debug(f'get to change values: {values}')
    logger.debug(f'photo {photo}')
    if values:
        if 'login' in values:
            rename_dir_of_login(
                old=user.login,
                new=values['login'],
            )
        for name, value in values.items():
            setattr(user, name, value)
        await session.commit()
    if photo:
        new_file = await rm_save_upload_file(
            old=user.picture,
            file=photo,
            login=user.login,
        )
        user.picture = new_file
        await session.commit()
        logger.debug(
        f'has update user {user.id} {user.login}: {user}',
        )
    return user_schema.model_dump(exclude_none=True, exclude_unset=True)


@logger.catch(reraise=True)
async def delete_user(user: User,
                      session: AsyncSession,
                      ):
    logger.debug(f'try delete user {user.id} {user.login} {user}')
    delete_dir(user.login)
    if not user.is_admin:
        await session.delete(user)
        await session.commit()
        logger.debug('user has delete')
