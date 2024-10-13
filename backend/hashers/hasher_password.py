import bcrypt

from pydantic import BaseModel


class PasswordHasher(BaseModel):
    """
    Класс хеширования паролей
    """
    password: str

    def _get_salt(self,
                  rounds: int = 12,
                  prefix: bytes = b"2b",
                  ) -> bytes:
        return bcrypt.gensalt(rounds=rounds,
                              prefix=prefix,
                              )

    def _hash_password(self,
                       password: str,
                       ) -> bytes:
        salt: bytes = self._get_salt()
        password_bytes: bytes = encode_password(
            password=password,
        )
        hashed_password: bytes = bcrypt.hashpw(
            password=password_bytes,
            salt=salt,
        )
        return hashed_password

    def get_hashed_password(self):
        """
        Получение хэшированного пароля
        """
        hash_password: bytes = self._hash_password(
            password=self.password,
        )
        return hash_password


class PasswordHashCheker(BaseModel):
    """
    Класс проверки хэшированных паролей
    """
    password: str
    hash_password: bytes

    def _check_password(self,
                        password: str,
                        hash_password: bytes,
                        ) -> bool:
        password_bytes: bytes = encode_password(
            password=password,
        )
        is_correct: bool = bcrypt.checkpw(
            password=password_bytes,
            hashed_password=hash_password,
        )
        return is_correct
    
    def is_correct(self) -> bool:
        """
        Проверка паролей на совпадение
        """
        is_correct: bool = self._check_password(
            password=self.password,
            hash_password=self.hash_password,
        )
        return is_correct


def encode_password(password: str,
                    codec: str = 'utf-8',
                    ) -> bytes:
    password_bytes: bytes = password.encode(encoding=codec)
    return password_bytes
