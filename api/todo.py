from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from cache.service import RedisTodoService
from models.todo import Todo
from schemas.base import APIException
from schemas.todo import TodoOut, TodoIn
from services.todo import TodoService

router = APIRouter(
    prefix="/todo",
    tags=["Todo Item"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo: TodoIn,
        todo_service: Annotated[TodoService, Depends()],
        redis_service: Annotated[RedisTodoService, Depends()],
) -> TodoOut:
    created_todo = await todo_service.create(Todo(**todo.model_dump()))
    created_todo_pydantic = TodoOut.model_validate(
        created_todo,
        from_attributes=True,
    )

    # Add item to Redis
    await redis_service.add_todo(created_todo_pydantic)

    return created_todo_pydantic


@router.get("/")
async def list_todos(
        todo_service: Annotated[TodoService, Depends()],
) -> list[TodoOut]:
    todos = await todo_service.list()
    pydantic_todos = [
        TodoOut.model_validate(todo, from_attributes=True)
        for todo in todos
    ]

    return pydantic_todos


@router.get("/{todo_id}", responses={404: {"model": APIException}})
async def get_todo(
        todo_id: int,
        todo_service: Annotated[TodoService, Depends()],
        redis_service: Annotated[RedisTodoService, Depends()],
) -> TodoOut:
    # Check item in Redis
    todo = await redis_service.get_todo(todo_id)
    # If it's None get item from DB
    if todo is None:
        todo = await todo_service.get(todo_id)
        if todo is None:
            raise HTTPException(404, "Todo not found")

        pydantic_todo = TodoOut.model_validate(todo, from_attributes=True)
        # Add item to Redis
        await redis_service.add_todo(pydantic_todo)
        return pydantic_todo

    return todo


@router.put("/{todo_id}", responses={404: {"model": APIException}})
async def put_todo(
        todo_id: int,
        todo: TodoIn,
        todo_service: Annotated[TodoService, Depends()],
        redis_service: Annotated[RedisTodoService, Depends()],
) -> TodoOut:
    todo_updated = await todo_service.update(todo_id, todo)

    pydantic_todo_existed = TodoOut.model_validate(
        todo_updated, from_attributes=True
    )

    # Update item in Redis
    await redis_service.add_todo(pydantic_todo_existed)

    return pydantic_todo_existed


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": APIException}}
)
async def delete_todo(
        todo_id: int,
        todo_service: Annotated[TodoService, Depends()],
        redis_service: Annotated[RedisTodoService, Depends()],
) -> None:
    await todo_service.delete(todo_id)

    # Delete item from Redis
    await redis_service.delete_todo(todo_id)

    return
