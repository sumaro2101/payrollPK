from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    async_scoped_session,
                                    AsyncSession,
                                    )
from asyncio import current_task

from typing import Any, AsyncGenerator

from backend.config import settings


class DataBaseSetup:
    """
    Инициализация базы данных
    """
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.DB.url,
            echo=settings.DB.DEBUG,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    def _get_scoped_session(self):
        """
        Создание локальной сессии
        """
        session = async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )
        return session

    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session = self._get_scoped_session()
        yield session
        await session.remove()


db_setup = DataBaseSetup()
