from pydantic import BaseModel


class Create_customer_location(BaseModel):
    name: str
    map_long: str
    map_lat: str
    address: str
    orienter: str
    customer_id: int

class Update_customer_location(BaseModel):
    id: int
    name: str
    map_long: str
    map_lat: str
    address: str
    orienter: str
    customer_id: int
