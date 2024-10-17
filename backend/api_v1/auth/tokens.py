from pydantic import BaseModel, ConfigDict
from backend.api_v1.auth.utils import encode_jwt

from typing import ClassVar

from backend.config import settings
from backend.config.models import User


t_type = settings.AUTH_JWT.TOKEN_TYPE_FIELD


class Token(BaseModel):
    """
    Класс токена

    Преназначен для выпуска access токена
    и для refresh токена
    """
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              frozen=True,
                              )

    __name_type: ClassVar[str] = t_type
    __access_token: ClassVar[str] = settings.AUTH_JWT.ACCESS_TOKEN_TYPE
    __expite_access_token: ClassVar[int] = settings.AUTH_JWT.EXPIRE_MINUTES

    user: User

    def _create_jwt(self,
                    token_type: str,
                    payload: dict[str],
                    expire: int,
                    ) -> str:
        """
        Создание jwt токена
        """
        jwt_payload = {self.__name_type: token_type}
        jwt_payload.update(payload)
        token = encode_jwt(jwt_payload, expire=expire)
        return token

    def create_access_token(self) -> str:
        """
        Создание access токена
        """
        jwt_payload = dict(sub=self.user.login,
                           username=self.user.login,
                           )
        access_token = self._create_jwt(token_type=self.__access_token,
                                        payload=jwt_payload,
                                        expire=self.__expite_access_token,
                                        )
        return access_token
