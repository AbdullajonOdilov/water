from typing import List

from pydantic import BaseModel

from schemas.phones_schemas import CreatePhone, UpdatePhone


class CreateBranche(BaseModel):
    name: str
    address: str
    map_long: str
    map_lat: str
    status: bool
    phones: List[CreatePhone]


class UpdateBranche(BaseModel):
    id: int
    name: str
    address: str
    map_long: str
    map_lat: str
    status: bool
    phones: List[UpdatePhone]
