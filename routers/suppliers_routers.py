from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.suppliers_func import all_suppliers, create_supplier_e, update_supplier_e
from models.suppliers import Suppliers
from schemas.suppliers_schemas import CreateSuppliers, UpdateSuppliers
from utils.auth import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import *

suppliers_router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers operation"]
)


@suppliers_router.get("/get_suppliers")
def get_suppliers(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Suppliers, id)
    return all_suppliers(search, page, limit, db,branch_id)


@suppliers_router.post("/create_suppliers")
def create_suppliers(new_suppliers: CreateSuppliers, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    create_supplier_e(new_suppliers, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@suppliers_router.put("/update_suppliers")
def update_suppliers(this_suppliers: UpdateSuppliers, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_supplier_e(this_suppliers, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



