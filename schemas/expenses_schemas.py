from pydantic import BaseModel

class CreateExpenses(BaseModel):
    name: str
    money: int
    branch_id: int
    source: str
    source_id: int
    kassa_id: int
    comment: str
    type: str

class UpdateExpenses(BaseModel):
    id: int
    name: str
    money: int
    comment: str
    type: str