from sqlalchemy import String, text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseOrm
from models.base import int_pk


class Todo(BaseOrm):
    __tablename__ = "todo"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(100))
    is_completed: Mapped[bool] = mapped_column(server_default=text("False"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
