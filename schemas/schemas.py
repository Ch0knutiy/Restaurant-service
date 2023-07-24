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
