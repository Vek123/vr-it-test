import contextlib
import logging
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from cache import redis
from db import db_manager
from cache.redis import r
from settings import settings
from middleware import *


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    db_manager.init(settings.db_url)
    await redis.check_connection(logger)
    yield
    await db_manager.close()


app = FastAPI(title=settings.app_title, lifespan=lifespan)
app.include_router(
    api_router,
    prefix="/api",
)

# Setting up file logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)
file_handler = logging.FileHandler("logs/http_logs.log", "a")
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Add logging middleware
app.add_middleware(HTTPLogMiddleware, logger, RedisLogService(r))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
