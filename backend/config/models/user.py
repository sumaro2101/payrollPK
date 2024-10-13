from sqlalchemy.orm import Mapped, mapped_column, composite, relationship
from sqlalchemy.types import LargeBinary, DECIMAL
from sqlalchemy import String, Unicode, func, ForeignKey
from sqlalchemy_utils import PhoneNumber

from typing import TYPE_CHECKING

from datetime import datetime

from .mixins import UserRelationMixin
from backend.config.models import Base

if TYPE_CHECKING:
    from backend.config.models import Position


class User(Base):
    """
    Модель пользователя
    """
    login: Mapped[str] = mapped_column(unique=True)
    picture: Mapped[str | None] = mapped_column(default=None)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(70))
    middle_name: Mapped[str] = mapped_column(String(70),
                                             nullable=True,
                                             )
    password: Mapped[str] = mapped_column(LargeBinary)
    salary: Mapped[float] = mapped_column(DECIMAL(12, 2))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now(),
                                                  server_default=func.now(),
                                                  )
    login_date: Mapped[datetime | None] = mapped_column(default=None,
                                                        server_default=None,
                                                        nullable=True,
                                                        )
    active: Mapped[bool] = mapped_column(default=True)
    is_accountant: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    _phone_number: Mapped[str] = mapped_column(Unicode(20))
    country_code: Mapped[str] = mapped_column(Unicode(8))
    phone = composite(
        PhoneNumber,
        _phone_number,
        country_code,
    )
    position_id: Mapped[int | None] = mapped_column(ForeignKey('positions.id'))

    position: Mapped['Position'] = relationship(
        back_populates='users',
    )
