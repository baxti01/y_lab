import uuid

from pydantic import BaseModel


class BaseSubmenu(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    title: str
    description: str


class FullSubmenu(BaseSubmenu):
    dishes_count: int


class UpdateSubmenu(BaseModel):
    title: str
    description: str
