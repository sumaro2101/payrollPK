from fastapi import Depends

from backend.api_v1.auth import get_current_active_user
from backend.config.models.user import User
from .exeptions import raise_non_admin_user, raise_non_accountant_user


async def is_admin(admin: User = Depends(get_current_active_user)):
    if not admin.is_admin:
        raise_non_admin_user()
    return admin


async def is_accountant(accountant: User = Depends(get_current_active_user)):
    if accountant.is_accountant or accountant.is_admin:
        return accountant
    raise_non_accountant_user()
