from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    comment: str


class UpdateCategory(BaseModel):
    id: int
    name: str
    comment: str

