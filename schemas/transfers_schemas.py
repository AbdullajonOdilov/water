from datetime import date
from pydantic import BaseModel, validator, Field
from sqlalchemy import *


class CreateTransfer(BaseModel):
    warehouse_product_id: int
    quantity: int = Field(..., gt=0)
    order_id: int
    warehoueser_id: int
    driver_id: int
    status: bool
    
    # class Config:
    #     arbitrary_types_allowed = True
    #
    # @validator('date', pre=True)
    # def parse_date(cls, value):
    #         if isinstance(value, str):
    #             return date.fromisoformat(value)
    #         return value


class UpdateTransfer(BaseModel):
    id: int
    quantity: int = Field(..., gt=0)
    date: date
    warehoueser_id: int
    driver_id: int
    status: bool
    
    # class Config:
    #     arbitrary_types_allowed = True
    #
    # @validator('date', pre=True)
    # def parse_date(cls, value):
    #         if isinstance(value, str):
    #             return date.fromisoformat(value)
    #         return value