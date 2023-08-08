from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.categories_func import create_category_y, update_category_y, all_categories
from models.categories import Categories
from utils.auth import get_current_user
from utils.db_operations import get_in_db
from schemas.users_schemas import CreateUser
from schemas.categories_schemas import CreateCategory, UpdateCategory
from db import database
from utils.role_checker import role_admin, role_driver, role_operator, role_verification, role_warehouser



categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories operation"]
)


@categories_router.get("/get_categories")
def get_categories(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id : int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Categories, id)
    return all_categories(search, page, limit, db,branch_id)
    


@categories_router.post("/create_category")
def create_category(new_category: CreateCategory, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    create_category_y(new_category, db,current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.put("/update_category")
def update_category(this_category: UpdateCategory, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_category_y(this_category, db,current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






