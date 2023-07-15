from pydantic import BaseModel

class CreateTrade(BaseModel):
    name: str
    warehouse_pr_id: int
    quantity: int
    order_id: int


class UpdateTrade(BaseModel):
    id: int
    warehouse_pr_id: int
    quantity: int
    order_id: int