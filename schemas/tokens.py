from pydantic import BaseModel


class Token(BaseModel):
    id: int
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []