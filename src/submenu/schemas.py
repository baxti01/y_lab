import uuid
from typing import Optional

from pydantic import BaseModel


class BaseSubmenu(BaseModel):
    title: str
    description: str


class Submenu(BaseSubmenu):
    id: uuid.UUID = uuid.uuid4()
    dishes_count: Optional[int] = None


class FullSubmenu(Submenu):
    dishes_count: Optional[int] = None


class CreateSubmenu(BaseSubmenu):
    pass


class UpdateSubmenu(BaseSubmenu):
    pass
