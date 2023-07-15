from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    comment: str
    user_id: int

class UpdateCategory(BaseModel):
    id: int
    name: str
    comment: str
    user_id: int
