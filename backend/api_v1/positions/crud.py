from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, Insert, Delete, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from loguru import logger

from backend.config.models.position import Position
from backend.handlers.handle_error import sql_parse_error_message
from .schemas import (CreatePositionSchema,
                      UpdatePositionSchema,
                      )


async def get_position_id(position_id: int,
                          session: AsyncSession,
                          ) -> Position:
    stmt = (Select(Position)
            .where(Position.id == position_id)
            .options(selectinload(Position.users)))
    position = await session.execute(statement=stmt)
    return position.scalar()


async def get_list_position(session: AsyncSession) -> list[Position]:
    stmt = (Select(Position)
            .order_by(Position.name)
            .options(selectinload(Position.users)))
    positions = await session.execute(statement=stmt)
    return positions.scalars().all()


async def create_position(position_schema: CreatePositionSchema,
                          session: AsyncSession,
                          ) -> Position:
    logger.info(f'position_schema = {position_schema}')
    stmt = (Insert(Position)
            .values(**position_schema.model_dump())
            .returning(Position.id, Position.name))
    try:
        position = await session.execute(stmt)
        await session.commit()
    except IntegrityError as ex:
        error = sql_parse_error_message(ex=ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(position=error))
    return position.first()


async def update_position(position_id: int,
                          position_schema: UpdatePositionSchema,
                          session: AsyncSession,
                          ) -> Position:
    stmt = (Update(Position)
            .where(Position.id == position_id)
            .values(position_schema.model_dump(exclude_unset=True))
            .returning(Position.id, Position.name))
    position = await session.execute(statement=stmt)
    await session.commit()
    result = position.first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(position_id=f'Position with id {position_id} is not found'),
                            )
    return result


async def delete_position(position_id: int,
                          session: AsyncSession,
                          ) -> None:
    stmt = (Delete(Position)
            .where(Position.id == position_id))
    try:
        await session.execute(statement=stmt)
        await session.commit()
    except IntegrityError as ex:
        error = sql_parse_error_message(ex=ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(delete=error))
    return None
