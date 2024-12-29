import json
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from cache.redis import get_redis
from schemas.todo import TodoOut


class BaseRedisService:
    def __init__(self, redis: Annotated[Redis, Depends(get_redis)]):
        self.redis = redis


class RedisTodoService(BaseRedisService):
    async def get_todo(self, todo_id: int) -> TodoOut | None:
        todo = await self.redis.get(f"todo:{todo_id}")
        if todo is None:
            return None
        todo = TodoOut.model_validate_json(todo)
        return todo

    async def get_all_todo(self) -> list[TodoOut]:
        todo_keys = await self.redis.scan(0, "todo:*")
        result = [await self.redis.get(todo) for todo in todo_keys[1]]
        return [TodoOut.model_validate_json(todo) for todo in result]

    async def add_todo(self, todo: TodoOut) -> None:
        await self.redis.setex(f"todo:{todo.id}", 10, todo.model_dump_json())

    async def delete_todo(self, todo_id: int) -> None:
        await self.redis.delete(f"todo:{todo_id}")


class RedisLogService(BaseRedisService):
    async def add_log(self, log: dict) -> None:
        await self.redis.rpush("log:http", json.dumps(log))

    async def get_logs(self) -> list[dict]:
        raw_logs = await self.redis.lrange("log:http", 1, -1)
        return [json.loads(log) for log in raw_logs]
