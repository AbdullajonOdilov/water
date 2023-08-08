import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.orders_func import all_orders, create_order_r, update_order_r, delete_order_r
from models.orders import Orders
from utils.auth import get_current_active_user
from utils.db_operations import get_in_db
from schemas.orders_schemas import CreateOrder, UpdateOrder
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import role_admin, role_driver, role_operator, role_verification,role_warehouser

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders operation"]
)


@orders_router.get("/get_orders")
def get_orders(search: str = None, id: int = 0, page: int = 0, limit: int = 25,
               db: Session = Depends(database),
               current_user: CreateUser = Depends(get_current_active_user),
               branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Orders, id)
    return all_orders(search, page, limit, db, branch_id)


@orders_router.post("/create_order")
async def create_order(new_order: CreateOrder, db: Session = Depends(database),
                       current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    await create_order_r(new_order, db, current_user)
    raise HTTPException(status_code=201, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.put("/update_order")
async def update_order(this_order: UpdateOrder, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    await update_order_r(this_order, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.delete("/delete_order")
def delete_order(id: int, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    delete_order_r(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






