from datetime import date
from pydantic import BaseModel, validator, Field
from sqlalchemy import *


class CreateTransfer(BaseModel):
    warehouse_product_id: int
    quantity: int = Field(..., gt=0)
    order_id: int
    warehouser_id: int
    driver_id: int
    status: bool


class UpdateTransfer(BaseModel):
    id: int
    quantity: int = Field(..., gt=0)
    warehouser_id: int
    driver_id: int
    status: bool
