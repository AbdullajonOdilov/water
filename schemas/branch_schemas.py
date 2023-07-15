from typing import List

from pydantic import BaseModel

from schemas.phones_schemas import CreatePhone, UpdatePhone


class CreateBranche(BaseModel):
    name: str
    adress: str
    map_long: str
    map_lat: str
    status: str
    phones: List[CreatePhone]


class UpdateBranche(BaseModel):
    id: int
    name: str
    adress: str
    map_long: str
    map_lat: str
    status: str
    phones: List[UpdatePhone]
