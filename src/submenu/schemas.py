import uuid

from pydantic import BaseModel


class BaseSubmenu(BaseModel):
    title: str
    description: str


class Submenu(BaseSubmenu):
    id: uuid.UUID
    menu_id: uuid.UUID
    dishes_count: int | None = 0

    class Config:
        from_attributes = True


class CreateSubmenu(BaseSubmenu):
    pass


class UpdateSubmenu(BaseSubmenu):
    pass
