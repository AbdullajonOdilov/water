from pydantic import BaseModel


class CreateProducts(BaseModel):
    name: str
    comment: str
    price: int
    category_id: int


class UpdateProducts(BaseModel):
    id: int
    name: str
    comment: str
    price: int
    category_id: int