from pydantic import BaseModel


class Base(BaseModel):
    ...


class APIException(Base):
    detail: str
