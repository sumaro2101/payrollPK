from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config
from pathlib import Path
from functools import partial
import os


BASE_DIR = Path(__file__).parent.parent

IMAGE_URL = partial(os.path.join, 'backend', 'images')

CERTS_DIR = BASE_DIR / 'certs'

config = Config('.env')


class Logging(BaseModel):
    FORMAT: str = '{time} {level} {message}'
    LOGGER_LOG: str = config('LOGGER_LOG')
    LOGGER_LEVEL: str = config('LOGGER_LEVEL')
    LOGGER_ROTATION: str = config('LOGGER_ROTATION')
    LOGGER_COMPRESSION: str = config('LOGGER_COMPRESSION')


class AuthJWT(BaseModel):
    PRIVATE_KEY_PATH: Path = CERTS_DIR / 'jwt-private.pem'
    PUBLIC_KEY_PATH: Path = CERTS_DIR / 'jwt-public.pem'
    ALGORITHM: str = config('ALGORITHM_JWT_AUTH')
    EXPIRE_MINUTES: int = 60 * 2
    REFRESH_EXPIRE_MINUTES: int = ((60 * 24) * 30)
    TOKEN_TYPE_FIELD: str = 'type'
    ACCESS_TOKEN_TYPE: str = 'access'


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
    LOGGING: Logging = Logging()
    ALLOW_HOST: str = config('ALLOW_HOST')
    AUTH_JWT: AuthJWT = AuthJWT()

settings = Settings()
