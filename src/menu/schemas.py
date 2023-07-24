import uuid

from pydantic import BaseModel


class BaseMenu(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    title: str
    description: str


class FullMenu(BaseMenu):
    submenu_count: int
    dishes_count: int


class UpdateMenu(BaseModel):
    title: str
    description: str

