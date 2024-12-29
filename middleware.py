import time
from logging import Logger

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from cache.service import RedisLogService
from utils import HTTPLog


class HTTPLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: Logger, redis: RedisLogService):
        super().__init__(app)
        self.logger = logger
        self.redis = redis

    async def dispatch(self, request: Request, call_next):
        log = HTTPLog(str(request.url), request.method, request.headers.raw)
        log_dict = log.to_dict()
        log_dict.pop("headers")
        self.logger.info(log.to_str())

        start = time.time()
        response = await call_next(request)
        time_to_response = time.time() - start

        log_dict["time_to_response"] = time_to_response

        await self.redis.add_log(log_dict)

        return response
