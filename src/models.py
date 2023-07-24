from decimal import Decimal
from sqlalchemy import Column, Uuid, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Uuid, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    submenus = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete"
    )


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(Uuid, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    menu_id = Column(ForeignKey("menu.id", ondelete="CASCADE"))
    menu = relationship("Menu", back_populates="submenus")

    dishes = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete"
    )


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Uuid, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), default=Decimal(0.0))

    submenu_id = Column(ForeignKey("submenu.id", ondelete="CASCADE"))
    submenu = relationship("Submenu", back_populates="dishes")
