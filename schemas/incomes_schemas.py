from pydantic import BaseModel, Field


class CreateIncome(BaseModel):
    money: float
    comment: str
    kassa_id: int
    source: str


class UpdateIncome(BaseModel):
    id: int
    money: float
    comment: str
    kassa_id: int
    source: str
    