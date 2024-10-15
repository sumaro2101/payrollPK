from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import TYPE_CHECKING

from backend.config.models import Base

if TYPE_CHECKING:
    from backend.config.models import User


class Position(Base):
    """
    Модель должности
    """
    name: Mapped[str] = mapped_column(String(70),
                                      unique=True,
                                      )

    users: Mapped[list['User']] = relationship(
        'User',
        back_populates='position',
    )
