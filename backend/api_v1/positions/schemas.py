from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    is_accountant: bool
    active: bool
    picture: str
    salary: Decimal = Field(max_digits=12,
                            decimal_places=2,
                            gt=0,
                            )
    phone: str
    create_date: datetime
    login_date: datetime | None = Field(default=None)


class BasePositionSchema(BaseModel):
    """
    Базовая схема должности
    """
    model_config = ConfigDict(from_attributes=True)

    name: str


class CreatePositionSchema(BasePositionSchema):
    """
    Схема создания должности
    """


class UpdatePositionSchema(BasePositionSchema):
    """
    Схема обновления должности
    """


class PositionSchema(BasePositionSchema):
    """
    Схема должности
    """
    id: int


class PositionSchemaUsers(PositionSchema):
    """
    Схема должности
    """
    users: list[UserSchema]
