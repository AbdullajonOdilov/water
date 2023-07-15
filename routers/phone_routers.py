import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.phones_func import all_phones
from models.phones import Phones
from utils.auth import get_current_user
from utils.db_operations import get_in_db
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import role_admin, role_verification

phones_router = APIRouter(
    prefix="/phones",
    tags=["Phones operation"]
)


@phones_router.get("/get_phones")
def get_phones(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Phones, id)
    return all_phones(search, page, limit, db,branch_id)
