from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.customer_loc_products_func import all_customer_loc_products,create_customer_loc_product_y,\
    update_customer_loc_product_y
from models.customer_loc_pro import Customer_loc_products
from utils.auth import get_current_active_user
from utils.db_operations import get_in_db
from schemas.customer_loc_products_schemas import CreateCustomerLocProducts, UpdateCustomerLocProducts
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import role_admin, role_driver, role_operator, role_verification, role_warehouser

customer_loc_products_router = APIRouter(
    prefix="/cus_locproducts",
    tags=["Customer Loc Products operation"]
)


@customer_loc_products_router.get("/get_products")
def get_products(search: str = None, id: int = 0,
                 page: int = 0, limit: int = 25,
                 db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user),
                 branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Customer_loc_products, id)
    return all_customer_loc_products(search, page, limit, db,branch_id)


@customer_loc_products_router.post("/create_loc_product")
def create_product(new_loc_product: CreateCustomerLocProducts, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    create_customer_loc_product_y(new_loc_product, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@customer_loc_products_router.put("/update_loc_product")
def update_product_loc(this_order: UpdateCustomerLocProducts, db: Session = Depends(database),
                        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_customer_loc_product_y(this_order, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


# @customer_loc_products_router.delete("/delete_product")
# def delete_product(id: int, db: Session = Depends(database),
#                 current_user: CreateUser = Depends(get_current_user)):
#     role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
#     delete_order_r(id, db)
#     raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






