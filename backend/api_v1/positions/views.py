from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from backend.config.models.position import Position
from backend.config.models.user import User

from .schemas import (CreatePositionSchema,
                      PositionSchema,
                      PositionSchemaUsers,
                      UpdatePositionSchema,
                      )
from backend.config.db import db_setup
from .permissions import is_accountant
from . import crud
from .dependencies import get_position
from backend.api_v1.auth import get_active_user


router = APIRouter(prefix='/positions',
                   tags=['Positions'],
                   )


@router.get(path='/list',
            response_model=list[PositionSchemaUsers])
async def get_list_positions(user: User = Depends(get_active_user),
                             session: AsyncSession = Depends(db_setup.get_session),
                             ):
    return await crud.get_list_position(session=session)


@router.put(path='/create',
            response_model=PositionSchema,
            status_code=status.HTTP_201_CREATED,)
async def create_position(position_schema: CreatePositionSchema,
                          accountant: User = Depends(is_accountant),
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.create_position(
        position_schema=position_schema,
        session=session,
    )


@router.get(path='/{position_id}',
            response_model=PositionSchemaUsers,
            )
async def get_position(user: User = Depends(get_active_user),
                       position: Position = Depends(get_position),
                       ):
    return position


@router.patch(path='/update/{position_id}',
              response_model=PositionSchema,
              )
async def update_position(position_id: int,
                          position_schema: UpdatePositionSchema,
                          accountant: User = Depends(is_accountant),
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.update_position(
        position_id=position_id,
        position_schema=position_schema,
        session=session,
    )


@router.delete(path='/delete/{position_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_position(position_id: int,
                          accountant: User = Depends(is_accountant),
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.delete_position(
        position_id=position_id,
        session=session,
    )
