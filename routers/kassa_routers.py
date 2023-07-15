from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.branch_func import all_branches, create_branche_r, update_branche_r
from functions.kassa_func import all_kassa_r, create_kassa_r
from models.branches import Branches
from utils.auth import get_current_user
from schemas.kassa_schemas import CreateKassa
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from schemas.branch_schemas import CreateBranche,UpdateBranche
from db import database
from utils.role_checker import role_admin, role_verification

kassas_router = APIRouter(
    prefix="/kassas",
    tags=["Kassas operation"]
)


@kassas_router.get("/get_kassas")
def get_kassas(search: str = None, id: int = 0, page: int = 0, limit: int = 25, status: str = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Branches, id)
    return all_kassa_r(search, page, limit,db,branch_id)
@kassas_router.post("/create_kassas")
def create_kassas(new_kassa: CreateKassa,db: Session = Depends(database),current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    create_kassa_r(new_kassa,db,current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
