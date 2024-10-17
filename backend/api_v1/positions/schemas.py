from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class UserSchemaView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    name: str
    surname: str
    middle_name: str | None
    is_accountant: bool
    active: bool
    picture: str | None
    phone_number: str = Field(alias='_phone_number')
    create_date: datetime
    login_date: datetime | None


class AccountantShemaView(UserSchemaView):
    salary: Decimal | None = Field(max_digits=12,
                        decimal_places=2,
                        gt=0,
                        )


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
    users: list[UserSchemaView | AccountantShemaView]
