from datetime import date
from pydantic import BaseModel, validator
from sqlalchemy import *


class CreateTransfer(BaseModel):
    name: str
    product_id: int
    quantity: int
    date: date
    warehoueser_id: int
    driver_id: int
    status: str
    
    class Config:
        arbitrary_types_allowed = True

    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value

class UpdateTransfer(BaseModel):
    id: int
    name: str
    quantity: int
    date: date
    warehoueser_id: int
    driver_id: int
    status: str
    
    class Config:
        arbitrary_types_allowed = True

    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value