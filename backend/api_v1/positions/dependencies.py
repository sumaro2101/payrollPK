from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_position_id
from backend.config.db import db_setup


async def get_position(position_id: int,
                       session: AsyncSession = Depends(db_setup.get_session),
                       ):
    position = await get_position_id(position_id=position_id,
                                    session=session,
                                    )
    if not position:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(position_id=f'Position is not found'),
                            )
    return position
