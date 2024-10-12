from fastapi import APIRouter

from .users.views import router as users
from .positions.views import router as positions

router = APIRouter(prefix='/api/v1')

router.include_router(users)
router.include_router(positions)
