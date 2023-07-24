import uuid
from typing import Optional

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str


class Menu(BaseMenu):
    id: uuid.UUID

    submenus_count: Optional[int] = None
    dishes_count: Optional[int] = None


class FullMenu(Menu):
    submenus_count: int
    dishes_count: int


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
