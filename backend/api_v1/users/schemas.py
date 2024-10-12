from datetime import datetime
import json
from pydantic import (BaseModel,
                      ConfigDict,
                      Field,
                      model_validator,
                      )

from decimal import Decimal

from backend.api_v1.positions import BasePositionSchema


class BaseUserSchema(BaseModel):
    """
    Базовая схема пользователя
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    login: str
    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    is_accountant: bool
    active: bool


class UserSchemaVision(BaseUserSchema):
    """
    Схема для пользователя
    """
    id: int
    phone_number: str = Field(alias='_phone_number',
                              min_length=10,
                              max_length=20,
                              )
    position: BasePositionSchema


class AccountantSchemaVision(BaseUserSchema):
    """
    Схема для бухгалтера
    """
    id: int
    salary: Decimal = Field(max_digits=12,
                            decimal_places=2,
                            gt=0,
                            )
    position: BasePositionSchema
    phone_number: str = Field(alias='_phone_number',
                              min_length=10,
                              max_length=20,
                              )
    create_date: datetime
    login_date: datetime | None = Field(default=None)


class CreateUserSchema(BaseUserSchema):
    """
    Схема создания пользователя
    """
    salary: Decimal = Field(max_digits=12,
                            decimal_places=2,
                            gt=0,
                            )
    position_id: int = Field(gt=0)
    country_code: str = Field(default='RU')
    phone_number: str = Field(default='9006001000')
    password_1: str
    password_2: str
    
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UpdateUserSchema(BaseUserSchema):
    """
    Схема обновления пользователя
    """
    salary: Decimal = Field(max_digits=12,
                            decimal_places=2,
                            gt=0,
                            )
    position_id: int = Field(gt=0)
    country_code: str
    phone_number: str
