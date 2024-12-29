from copy import copy
from typing import Annotated, Sequence, Optional, Type

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.todo import Todo


class TodoService:
    def __init__(
            self,
            session: Annotated[AsyncSession, Depends(get_session)],
    ):
        self.session = session

    async def create(self, todo: Todo) -> Todo:
        self.session.add(todo)
        await self.session.commit()

        query = select(Todo).order_by(Todo.id.desc()).limit(1)
        created_todo = (await self.session.execute(query)).scalar_one()

        return created_todo

    async def get(self, todo_id: int) -> Optional[Todo]:
        todo = await self.session.get(Todo, todo_id)

        return todo

    async def list(self) -> Sequence[Todo]:
        query = select(Todo).order_by(Todo.id.asc())
        todos = (await self.session.execute(query)).scalars().all()

        return todos

    async def update(self, todo_id: int, todo: Todo) -> Type[Todo]:
        todo_existed = await self.session.get(Todo, todo_id)
        if todo_existed is None:
            raise HTTPException(404, "Todo not found")

        if todo.created_at:
            todo_existed.created_at = todo.created_at

        todo_existed.title = todo.title
        todo_existed.is_completed = todo.is_completed
        todo_existed_copy = copy(todo_existed)
        await self.session.commit()

        return todo_existed_copy

    async def delete(self, todo_id: int) -> None:
        existed_todo = await self.session.get(Todo, todo_id)
        if existed_todo is None:
            raise HTTPException(404, "Todo not found")

        await self.session.delete(existed_todo)
        await self.session.commit()

        return
