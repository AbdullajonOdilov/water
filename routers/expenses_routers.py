from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from functions.expenses_func import all_expenses, create_expenses_y, update_expenses_y
from models.expenses import Expenses
from utils.auth import get_current_active_user
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from schemas.expenses_schemas import CreateExpenses, UpdateExpenses
from db import database
from utils.role_checker import *

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses operation"]
)


@expenses_router.get("/get_expenses")
def get_expenses(search: str = None, id: int = 0,
                 page: int = 0, limit: int = 25,
                 db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user),
                 branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Expenses, id)
    return all_expenses(search, page, limit, db,branch_id)


@expenses_router.post("/create_expenses")
def create_products(new_expenses: CreateExpenses, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    create_expenses_y(new_expenses, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@expenses_router.put("/update_expenses")
def update_expenses(this_expenses: UpdateExpenses, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_expenses_y(this_expenses, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






