from pydantic import BaseModel, Field


class CreateIncome(BaseModel):
    money: float = Field(..., gt=0)
    comment: str
    kassa_id: int
    source: str
    source_id: int


class UpdateIncome(BaseModel):
    id: int
    money: float = Field(..., gt=0)
    comment: str
    kassa_id: int
    source: str
    source_id: int
    