from fastapi import status, HTTPException


def raise_non_admin_user():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Permission denied',
    )


def raise_non_accountant_user():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Permission denied',
    )
