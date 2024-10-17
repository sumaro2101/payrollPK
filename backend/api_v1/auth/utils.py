from typing import Any
import jwt
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status

from backend.config.models import User

from backend.config import settings


def encode_jwt(payload: dict[str, Any],
                private_key: str | bytes = settings.AUTH_JWT.PRIVATE_KEY_PATH.read_text(encoding='UTF-8'),
                algorithm: str | None = settings.AUTH_JWT.ALGORITHM,
                expire: int = settings.AUTH_JWT.EXPIRE_MINUTES,
                expire_minutes: timedelta | None = None
                ):
    """
    JWT кодировка ключа
    """
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_minutes:
        expire = now + expire_minutes
    else:
        expire = now + timedelta(minutes=expire)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(payload=to_encode,
                         key=private_key,
                         algorithm=algorithm,
                         )
    return encoded


def decode_jwt(jwt_key: str | bytes,
                key: str | bytes = settings.AUTH_JWT.PUBLIC_KEY_PATH.read_text(encoding='UTF-8'),
                algorithms: str = settings.AUTH_JWT.ALGORITHM,
                ):
    """
    JWT декодировка ключа
    """
    decoded = jwt.decode(jwt=jwt_key,
                         key=key,
                         algorithms=algorithms,
                         )
    return decoded


def check_type_token(token: str, type_token: str) -> None:
    if token and token != type_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=dict(user=f'Не верный тип токена, ожидался - {type_token}'),
                            )
