from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from functions.customers_func import all_customers, create_customers_y, update_customers_y
from models.customers import Customers
from utils.auth import get_current_user
from schemas.customers_schemas import Create_customer, Update_customer
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from db import database
from utils.role_checker import *

customers_routers = APIRouter(
    prefix="/customers",
    tags=["Customers Operations"]
)
@customers_routers.get("/get_customers")
def get_customers(search: str = None, id: int = 0, page: int = 0, limit: int = 25, type: str = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Customers, id)
    return all_customers(search, page, limit, db,branch_id)


@customers_routers.post("/create_customer")
def create_customer(new_customer: Create_customer, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    create_customers_y(new_customer, db, current_user)
    
@customers_routers.put("/update_customers")
def update_customers(this_customer: Update_customer, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_customers_y(this_customer, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

