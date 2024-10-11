from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config


config = Config('.env')


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    

settings = Settings()
