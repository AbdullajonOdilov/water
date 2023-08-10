from pydantic import BaseModel, Field


class CreateProducts(BaseModel):
    name: str
    comment: str
    price: int
    litr: float = Field(..., gt=0)
    category_id: int


class UpdateProducts(BaseModel):
    id: int
    name: str
    comment: str
    price: int
    litr: float = Field(..., gt=0)
    category_id: int