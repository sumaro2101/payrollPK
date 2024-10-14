from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config
from pathlib import Path
from functools import partial
import os


BASE_DIR = Path(__file__).parent.parent

IMAGE_URL = partial(os.path.join, 'backend', 'images')


config = Config('.env')


class DBSettings(BaseModel):
    _engine: str = config('DB_ENGINE')
    _owner: str = config('DB_USER')
    _password: str = config('DB_PASSWORD')
    _name: str = config('DB_HOST')
    _db_name: str = config('DB_NAME')
    _db_test: str = config('DB_TEST')
    DEBUG: bool = bool(int(config('DB_DEBUG')))
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'
    test_url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_test}'


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    DB: DBSettings = DBSettings()
    url_staticfiles: Path = '/backend/static'
    directory: Path = 'backend/static'
    staticname: str = 'static'
    url_images: Path = BASE_DIR / 'images'
    ADMIN_LOGIN: str = config('ADMIN_LOGIN')
    ADMIN_PASSWORD: str = config('ADMIN_PASSWORD')

settings = Settings()
