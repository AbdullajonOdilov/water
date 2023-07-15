from pydantic import BaseModel

class CreateCustomerLocProducts(BaseModel):
    name: str
    customer_loc_id: int
    product_id: int
    quantity: int

class UpdateCustomerLocProducts(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int