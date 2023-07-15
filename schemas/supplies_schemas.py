from datetime import date
from typing import List
from pydantic import BaseModel, validator
from sqlalchemy import *

class CreateSupplies(BaseModel):
    name: str
    product_id: int
    quantity: int
    price: int
    date: date
    warehouse_id: int
    supplier_id: int

    class Config:
        arbitrary_types_allowed = True

    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value


class UpdateSupplies(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int
    price: int
    date: date
    supplier_id: int

    class Config:
        arbitrary_types_allowed = True
    
    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value
