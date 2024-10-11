from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config


config = Config('.env')


class DBSettings(BaseModel):
    _engine: str = config('DB_ENGINE')
    _owner: str = config('DB_USER')
    _password: str = config('DB_PASSWORD')
    _name: str = config('DB_HOST')
    _db_name: str = config('DB_NAME')
    DEBUG: bool = bool(int(config('DB_DEBUG')))
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    DB: DBSettings = DBSettings()


settings = Settings()
