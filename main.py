from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.config.db import db_setup
from backend.config.models import Base
from backend.api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_setup.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await db_setup.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
