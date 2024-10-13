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
    UserSchemaVision,
    )
from backend.config.db import db_setup
from backend.api_v1.auth import get_active_user
from . import crud
from .permissions import is_admin, is_accountant


router = APIRouter(prefix='/users',
                   tags=['Users'],
                   )


@router.get(path='/get/list/',
            description='Получение списка пользователей',
            )
async def get_list_users(user: User = Depends(get_active_user),
                         session: AsyncSession = Depends(db_setup.get_session),
                         ) -> list[AccountantSchemaVision] | list[UserSchemaVision]:
    """
    Энд поинт получения пользователей
    """
    return await crud.get_users(user=user,
                                session=session,
                                )


@router.get(path='/get/profile/',
            response_model=AccountantSchemaVision,
            description='Просмотр профиля текущего пользователя',
            )
async def get_profile(user: User = Depends(get_active_user)):
    return user


@router.get(path='/get/{user_id}/',
            description='Получение пользователя по ID',
            )
async def get_user(user: User = Depends(get_active_user),
                   user_seach: User = Depends(get_user_by_id),
                   ) -> AccountantSchemaVision | UserSchemaVision:
    """
    Энд поинт получения пользователя по ID
    """
    if user.is_admin or user.is_accountant or user.id == user_seach.id:
        return user_seach
    else:
        delattr(user_seach, 'salary')
        return user_seach


@router.put(path='/create/',
            response_model=ViewUserSchema,
            description='Создание пользователя',
            status_code=status.HTTP_201_CREATED,
            )
async def create_user(user_schema: CreateUserSchema,
                      accountant: User = Depends(is_accountant),
                      photo: UploadFile | str = '',
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    """
    Энд поинт создания пользователя
    """
    is_accountant: bool = False
    if photo:
        correct = check_format_file(photo.filename)
        if not correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(picture='Invalid format file'))
    return await crud.create_user(
        user_schema=user_schema,
        photo=photo,
        session=session,
        accountant=is_accountant,
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
    is_accountant: bool = True
    if photo:
        correct = check_format_file(photo.filename)
        if not correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(picture='Invalid format file'))
    return await crud.create_user(
        user_schema=user_schema,
        photo=photo,
        session=session,
        accountant=is_accountant,
    )


@router.patch(path='/update/{user_id}/',
              response_model=ViewUserSchema,
              description='Обновление пользователя',
              )
async def update_user(user_schema: UpdateUserSchema,
                      accountant: User = Depends(is_accountant),
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
async def delete_user(accountant: User = Depends(is_accountant),
                      user: User = Depends(get_user_by_id),
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    return await crud.delete_user(
        user=user,
        session=session,
    )
