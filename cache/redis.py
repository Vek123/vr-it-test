from logging import Logger

import redis.asyncio as redis

from settings import settings


r = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_todo_db_id,
    username=settings.redis_user,
    password=settings.redis_user_password,
)


def get_redis() -> redis.Redis:
    yield r


async def check_connection(logger: Logger):
    response = await r.ping()
    if response:
        logger.info("Redis: Connection established.")
    else:
        logger.error("Redis: Connection refused.")
