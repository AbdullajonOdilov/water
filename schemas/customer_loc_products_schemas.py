from pydantic import BaseModel, Field


class CreateCustomerLocProducts(BaseModel):
    customer_loc_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class UpdateCustomerLocProducts(BaseModel):
    id: int
    customer_loc_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)