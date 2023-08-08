from pydantic import BaseModel, Field
from sqlalchemy import *


class CreateSupplies(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    warehouse_id: int
    supplier_id: int


class UpdateSupplies(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    price: int = Field(..., gt=0)
    supplier_id: int
