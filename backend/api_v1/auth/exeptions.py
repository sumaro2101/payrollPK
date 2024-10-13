from fastapi import status, HTTPException


def raise_incorect_values():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect login or password',
        headers={"WWW-Authenticate": "Basic"},
    )


def raise_non_active_user():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User is not active',
    )
