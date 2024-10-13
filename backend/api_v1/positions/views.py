from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from backend.config.models.position import Position

from .schemas import (CreatePositionSchema,
                      PositionSchema,
                      PositionSchemaUsers,
                      UpdatePositionSchema,
                      )
from backend.config.db import db_setup
from . import crud
from .dependencies import get_position


router = APIRouter(prefix='/positions',
                   tags=['Positions'],
                   )


@router.get(path='/list/',
            response_model=list[PositionSchemaUsers])
async def get_list_positions(session: AsyncSession = Depends(db_setup.get_session)):
    return await crud.get_list_position(session=session)


@router.put(path='/create/',
            response_model=PositionSchema,
            status_code=status.HTTP_201_CREATED,)
async def create_position(position_schema: CreatePositionSchema,
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.create_position(
        position_schema=position_schema,
        session=session,
    )


@router.get(path='/{position_id}/',
            response_model=PositionSchemaUsers,
            )
async def get_position(position: Position = Depends(get_position)):
    return position


@router.patch(path='/update/{position_id}/',
              response_model=PositionSchema,
              )
async def update_position(position_id: int,
                          position_schema: UpdatePositionSchema,
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.update_position(
        position_id=position_id,
        position_schema=position_schema,
        session=session,
    )


@router.delete(path='/delete/{position_id}/',
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_position(position_id: int,
                          session: AsyncSession = Depends(db_setup.get_session),
                          ):
    return await crud.delete_position(
        position_id=position_id,
        session=session,
    )
