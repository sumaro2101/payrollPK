from fastapi import Depends

from backend.api_v1.auth import get_active_user
from backend.config.models.user import User
from .exeptions import raise_non_admin_user


async def is_admin(admin: User = Depends(get_active_user)):
    if not admin.is_admin:
        raise_non_admin_user()
    return admin
