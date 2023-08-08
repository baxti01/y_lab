import uuid

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str


class Menu(BaseMenu):
    id: uuid.UUID

    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        from_attributes = True


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
