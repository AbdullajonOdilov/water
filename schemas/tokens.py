from pydantic import BaseModel


class Token(BaseModel):
    id: int
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    username: str