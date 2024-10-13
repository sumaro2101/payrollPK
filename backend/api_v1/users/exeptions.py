from fastapi import status, HTTPException


def raise_non_admin_user():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Permission denied',
    )
