from fastapi import Depends

from backend.api_v1.auth.auth import get_current_active_user
from backend.api_v1.users.exeptions import raise_non_accountant_user
from backend.config.models.user import User


async def is_accountant(accountant: User = Depends(get_current_active_user)):
    if accountant.is_accountant or accountant.is_admin:
        return accountant
    raise_non_accountant_user()
