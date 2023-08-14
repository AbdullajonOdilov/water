import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.warehouse_products_func import all_warehouses_products, create_warehouse_products_e, \
    update_warehouse_products_e, one_w_p
from models.warehouse_products import Warehouses_products
from utils.auth import get_current_active_user
from utils.db_operations import the_one
from schemas.warehouse_products_schemas import Warehouse_products_update
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import *

warehouses_products_router = APIRouter(
    prefix="/warehouses_products",
    tags=["Warehouses products operation"]
)


@warehouses_products_router.get("/get_warehouses_products")
def get_warehouses(search: str = None, id: int = 0, page: int = 0,
                   limit: int = 25, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user),
                   branch_id: int = 0,warehouse_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return one_w_p(db, id)
    return all_warehouses_products(search, page, limit, db, branch_id, warehouse_id)


@warehouses_products_router.put("/update_warehouses_products")
def update_warehouse(this_warehouse: Warehouse_products_update, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_warehouse_products_e(this_warehouse, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






