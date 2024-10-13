from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi import (Path,
                     Depends,
                     HTTPException,
                     status,
                     )

from typing import Annotated

from backend.config.models import User
from backend.config.db import db_setup
from .schemas import (AccountantSchemaVision,
                      UserSchemaVision,
                      )


async def get_user_by_id(user_id: Annotated[int, Path(gt=0)],
                        session: AsyncSession = Depends(db_setup.get_session),
                        ) -> User:
    """
    Получение пользователя по ID
    """
    stmt = (Select(User).where(User.id == user_id)
            .options(selectinload(User.position)))
    user: User = await session.scalar(statement=stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(user=f'User with number {user_id} is not found'),
        )
    return user
