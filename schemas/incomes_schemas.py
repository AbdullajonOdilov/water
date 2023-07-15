from pydantic import BaseModel

class CreateIncome(BaseModel):
    name: str
    money: int
    comment: str
    kassa_id: int
    type: str
    source: str
    source_id: int

class UpdateIncome(BaseModel):
    id: int
    name: str
    money: int
    comment: str
    kassa_id: int
    type: str
    source: str
    source_id: int
    