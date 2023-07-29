from sqlalchemy import String, Column, ForeignKey, UUID, Integer
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    #submenus_count = Column(Integer(), nullable=False, default=0)
    #dishes_count = Column(Integer(), nullable=False, default=0)


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id", ondelete='CASCADE'))
    #dishes_count = Column(Integer(), nullable=False, default=0)


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(String(), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id", ondelete='CASCADE'))
