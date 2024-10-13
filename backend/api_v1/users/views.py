from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     status,
                     UploadFile,
                     )

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api_v1.regex import check_format_file
from backend.api_v1.users.dependencies import get_user_by_id
from backend.config.models.user import User
from backend.api_v1.users.schemas import (
    AccountantSchemaVision,
    CreateUserSchema,
    ViewUserSchema,
    UpdateUserSchema,
    )
from backend.config.db import db_setup
from . import crud
from .permissions import is_admin


router = APIRouter(prefix='/users',
                   tags=['Users'],
                   )


@router.get(path='/get/list/',
            response_model=list[AccountantSchemaVision],
            description='Получение списка пользователей',
            )
async def get_list_users(session: AsyncSession = Depends(db_setup.get_session)):
    """
    Энд поинт получения пользователей
    """
    return await crud.get_users(session=session)


@router.get(path='/get/{user_id}/',
            response_model=AccountantSchemaVision,
            description='Получение пользователя по ID',
            )
async def get_user(user: User = Depends(get_user_by_id)):
    """
    Энд поинт получения пользователя по ID
    """
    return user


@router.put(path='/create/',
            response_model=ViewUserSchema,
            description='Создание пользователя',
            status_code=status.HTTP_201_CREATED,
            )
async def create_user(user_schema: CreateUserSchema,
                      photo: UploadFile | str = '',
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    """
    Энд поинт создания пользователя
    """
    accountant: bool = False
    if photo:
        correct = check_format_file(photo.filename)
        if not correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(picture='Invalid format file'))
    return await crud.create_user(
        user_schema=user_schema,
        photo=photo,
        session=session,
        accountant=accountant,
    )


@router.put(path='/create/accountant/',
            response_model=ViewUserSchema,
            description='Создание бухгалтера (только админу)',
            status_code=status.HTTP_201_CREATED)
async def create_accountant(user_schema: CreateUserSchema,
                            admin: User = Depends(is_admin),
                            photo: UploadFile | str = '',
                            session: AsyncSession = Depends(db_setup.get_session),
                            ):
    """
    Энд поинт создания бухгалтера
    """
    accountant: bool = True
    if photo:
        correct = check_format_file(photo.filename)
        if not correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(picture='Invalid format file'))
    return await crud.create_user(
        user_schema=user_schema,
        photo=photo,
        session=session,
        accountant=accountant,
    )


@router.patch(path='/update/{user_id}/',
              response_model=ViewUserSchema,
              description='Обновление пользователя',
              )
async def update_user(user_schema: UpdateUserSchema,
                      user: User = Depends(get_user_by_id),
                      photo: UploadFile | str = '',
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    """
    Энд поинт обновления пользователя
    """
    if photo:
        correct = check_format_file(photo.filename)
        if not correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(picture='Invalid format file'))
    return await crud.update_user(
        user=user,
        user_schema=user_schema,
        photo=photo,
        session=session,
    )


@router.delete(path='/delete/{user_id}/',
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_user(user: User = Depends(get_user_by_id),
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    return await crud.delete_user(
        user=user,
        session=session,
    )
