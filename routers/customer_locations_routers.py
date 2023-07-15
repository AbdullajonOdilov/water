from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from functions.customer_loactions_functions import all_customer_locations,create_customer_locations_y, update_customer_loactions_y
from models.customers import Customers
from utils.auth import get_current_user
from schemas.customer_locations_schemas import Create_customer_location, Update_customer_location
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from db import database
from utils.role_checker import *

customers_locations_routers = APIRouter(
    prefix="/customers_locations",
    tags=["Customers Locations Operations"]
)
@customers_locations_routers.get("/get_customers_locations")
def get_customers(search: str = None, id: int = 0, page: int = 0, limit: int = 25, status: str = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Customers, id)
    return all_customer_locations(search, page, limit, db,branch_id)


@customers_locations_routers.post("/create_customers_locations")
def create_customer(new_customer_location: Create_customer_location, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    
    role_verification(user=current_user)
    create_customer_locations_y(new_customer_location, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

@customers_locations_routers.put("/update_customers_locations")
def update_customers_location(this_customer_location: Update_customer_location, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_customer_loactions_y(this_customer_location, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

