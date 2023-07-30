from uuid import UUID

from pydantic import BaseModel


class MenuSchema(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class SubmenuSchema(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class DishSchema(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        from_attributes = True


class EnrichedMenuSchema(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class EnrichedSubmenuSchema(BaseModel):
    id: UUID
    title: str
    description: str
    dishes_count: int
