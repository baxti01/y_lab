import uuid
from decimal import Decimal

from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str
    price: Decimal


class Dish(BaseDish):
    id: uuid.UUID
    submenu_id: uuid.UUID

    class Config:
        from_attributes = True


class CreateDish(BaseDish):
    pass


class UpdateDish(BaseDish):
    pass
