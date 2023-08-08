from pydantic import BaseModel, Field


class CreateExpenses(BaseModel):
    money: float = Field(..., gt=0)
    branch_id: int
    source: str
    source_id: int
    kassa_id: int
    comment: str


class UpdateExpenses(BaseModel):
    id: int
    money: float = Field(..., gt=0)
    comment: str