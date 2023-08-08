
from pydantic import BaseModel


class CreateOrder(BaseModel):

    driver_id: int
    warehouser_id: int
    customer_loc_id: int


class UpdateOrder(BaseModel):
    id: int
    status: int
    driver_id: int
    warehouser_id: int
    customer_loc_id: int

