from fastapi import APIRouter

from .users.views import router as users
from .positions.views import router as positions
from .auth.views import router as auth

router = APIRouter(prefix='/api/v1')

router.include_router(users)
router.include_router(positions)
router.include_router(auth)
