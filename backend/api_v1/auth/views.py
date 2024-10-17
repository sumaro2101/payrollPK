from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from backend.api_v1.auth.tokens import Token
from backend.config.db import db_setup
from .auth import get_authenticate


router = APIRouter(prefix='/auth',
                   tags=['Auth'],
                   )


@router.post(path='/login')
async def get_login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                         session: AsyncSession = Depends(db_setup.get_session)):
    user = await get_authenticate(form_data=form_data,
                                  session=session)
    token = Token(user=user)
    access = token.create_access_token()
    return {"access_token": access, "token_type": "Bearer"}
