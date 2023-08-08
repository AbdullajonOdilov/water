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

    # @validator('role', pre=True)
    # def validate_role_admin(cls, v):
    #     if v == 'admin' and cls.count_users_with_role(v) > 0:
    #         raise ValueError('Only one user can have the role "admin"')
    #     return v
    #
    # @classmethod
    # def count_users_with_role(cls, role, db: Session):
    #     count = db.query(Users).filter(Users.role == role).count()
    #
    #     return count


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
    balance_oylik: int
    phones: List[UpdatePhone]

    # @validator('role', pre=True)
    # def validate_role_admin(cls, v, values):
    #     db = values['db']  # Get the SQLAlchemy session from the values dictionary
    #     if v == 'admin' and cls.count_users_with_role(v, db) > 0:
    #         raise ValueError('Only one user can have the role "admin"')
    #     return v
    #
    # @classmethod
    # def count_users_with_role(cls, role, db: Session):
    #     count = db.query(Users).filter(Users.role == role).count()
    #
    #     return count

