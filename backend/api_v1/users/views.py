from fastapi import APIRouter, Depends, status, File, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from backend.api_v1.users.dependencies import get_user
from backend.config.models.user import User
from backend.api_v1.users.schemas import (
    AccountantSchemaVision,
    CreateUserSchema,
    )
from backend.config.db import db_setup
from . import crud


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
async def get_user(user: User = Depends(get_user)):
    """
    Энд поинт получения пользователя по ID
    """
    return user


@router.put(path='/create/',
            response_model=CreateUserSchema,
            description='Создание пользователя',
            status_code=status.HTTP_201_CREATED,
            )
async def create_user(user_schema: CreateUserSchema,
                      photo: UploadFile | None = None,
                      session: AsyncSession = Depends(db_setup.get_session),
                      ):
    """
    Энд поинт создания пользователя
    """
    return await crud.create_user(
        user_schema=user_schema,
        photo=photo,
        session=session,
    )
