from datetime import datetime
from typing import Optional

from pydantic import Field

from schemas.base import Base


class TodoIn(Base):
    title: str = Field(max_length=100)
    is_completed: Optional[bool] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)


class TodoOut(TodoIn):
    id: int
