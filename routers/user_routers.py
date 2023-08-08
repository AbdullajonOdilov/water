import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.user_functions import create_user_r, all_users, update_user_r
from models.users import Users
from utils.auth import get_current_user, get_current_active_user
from utils.db_operations import get_in_db
from schemas.users_schemas import CreateUser, UpdateUser
from db import database
from utils.role_checker import role_admin, role_verification

users_router = APIRouter(
    prefix="/users",
    tags=["Users operation"]
)


@users_router.get("/get_users")
def get_users(search: str = None, id: int = 0,
              page: int = 0, limit: int = 25,
              branch_id: int = 0,
              role: str = None,
              status: bool = None,  db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Users, id)
    return all_users(search, page, limit, status, branch_id, role, db)


@users_router.post("/create_user")
def create_user(new_user: CreateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)
                ):
    role_verification(user=current_user)
    create_user_r(new_user, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.put("/update_user")
def update_user(this_user: UpdateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_user_r(this_user, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.get("/request_user")
def request_user(current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user)
    return current_user
