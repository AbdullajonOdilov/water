from typing import List, Optional

from pydantic import BaseModel, validator
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from models.users import Users
from schemas.phones_schemas import CreatePhone, UpdatePhone


class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: bool
    balance_oylik: int
    branch_id: int
    phones: List[CreatePhone]


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
    balance_oylik: int
    phones: List[UpdatePhone]


