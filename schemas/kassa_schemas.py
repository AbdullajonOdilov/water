from typing import List
from pydantic import BaseModel

from schemas.phones_schemas import CreatePhone


class CreateKassa(BaseModel):
    name: str
    comment: str
    phones: List[CreatePhone]


class UpdateKassa(BaseModel):
    id: int
    name: str
    comment: str
    phones: List[CreatePhone]
