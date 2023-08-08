from pydantic import BaseModel, Field


class CreateUserProduct(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class UpdateUserProduct(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0)