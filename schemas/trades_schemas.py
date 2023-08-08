from pydantic import BaseModel, Field


class CreateTrade(BaseModel):
    warehouse_pr_id: int
    quantity: int = Field(..., gt=0)
    order_id: int


class UpdateTrade(BaseModel):
    id: int
    warehouse_pr_id: int
    quantity: int = Field(..., gt=0)
    order_id: int
