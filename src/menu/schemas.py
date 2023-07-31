import uuid
from typing import Optional

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str


class Menu(BaseMenu):
    id: uuid.UUID

    submenus_count: Optional[int] = 0
    dishes_count: Optional[int] = 0

    class Config:
        from_attributes = True


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
