from typing import List
from pydantic import BaseModel

from schemas.phones_schemas import CreatePhone, UpdatePhone

class Create_customer(BaseModel):
    name: str
    type: str
    comment: str
    balance: int
    phones: List[CreatePhone]


class Update_customer(BaseModel):
    id: int
    name: str
    type: str
    comment: str
    balance: int
    phones: List[UpdatePhone]

    