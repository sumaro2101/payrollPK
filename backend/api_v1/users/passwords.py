from pydantic import BaseModel
from fastapi import HTTPException, status


class PasswordsChecker(BaseModel):
    """Проверяет валидность паролей

    Args:
        password1 (str): Первый пароль
        password2 (str): Повторный пароль
    """
    password_1: str
    password_2: str

    def _check_leng_password(self, password: str) -> str:
        """
        Проверка длины пароля
        """
        if len(password) < 7:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(password='Password is too short'),
                                )
        return password

    def _check_similar_password(self,
                                password_1:str,
                                password_2: str,
                                ):
        """
        Проверка одинаковых паролей
        """
        if password_1 != password_2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(passwords='Differents passwords'),
                                )
        self._check_leng_password(password=password_1)

    def get_password(self) -> str:
        """
        Возвращает правильный пароль
        """
        self._check_similar_password(password_1=self.password_1,
                                     password_2=self.password_2,
                                     )
        password = self._check_leng_password(password=self.password_1)
        return password
