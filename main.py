import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from loguru import logger

from backend.config.db import db_setup
from backend.config.models import Base
from backend.config import settings
from backend.api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect = False
    while not connect:
        try:
            async with db_setup.engine.begin() as conn:
                connect = True
                await conn.run_sync(Base.metadata.create_all)
                yield
            await db_setup.dispose()
        except ConnectionRefusedError:
            logger.warning(
                f'No connect with DataBase, try 2 seconds leter',
                )
            time.sleep(2)


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.mount(
    settings.url_staticfiles.as_posix(),
    StaticFiles(directory=settings.directory),
    name=settings.staticname,
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOW_HOST],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)
