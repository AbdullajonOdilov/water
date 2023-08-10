from typing import List
from pydantic import BaseModel, Field


# class Warehouse_products_create(BaseModel):
#     product_id: int
#     quantity: int = Field(..., gt=0)
#     price: float = Field(..., gt=0)
#     warehouse_id: int
#

class Warehouse_products_update(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    warehouse_id: int
   