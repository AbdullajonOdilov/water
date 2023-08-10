from datetime import date
from pydantic import BaseModel, Field
from sqlalchemy import *


class CreateContract(BaseModel):
    warehouse_product_id: int
    quantity: int = Field(..., ge=0)
    deadline: int = Field(..., gt=0)


class UpdateContract(BaseModel):
    id: int
    warehouse_product_id: int
    quantity: int = Field(..., ge=0)
    deadline: int = Field(..., gt=0)
    status: bool
