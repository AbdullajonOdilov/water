from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint

from db import Base


class Token(BaseModel):
    acces_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
