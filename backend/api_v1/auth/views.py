from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from backend.config.models.user import User
from .auth import get_active_user


router = APIRouter(prefix='/auth',
                   tags=['Auth'],
                   )

@router.post(path='/login')
async def get_login_user(user: User = Depends(get_active_user)):
    return dict(state='success')
