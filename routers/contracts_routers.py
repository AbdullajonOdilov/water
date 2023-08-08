from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import database
from functions.contracts_func import all_contracts_r, create_contract_y, update_contract_y
from models.contracts import Contracts
from schemas.contracts_schemas import CreateContract, UpdateContract
from schemas.users_schemas import CreateUser
from utils.auth import get_current_active_user
from utils.db_operations import the_one
from utils.role_checker import *

contracts_router = APIRouter(
    prefix="/contracts",
    tags=["Contracts Operations"]
)


@contracts_router.get("/get_contracts")
def all_contracts(search: str = None, id: int = 0, page: int = 0,
                  limit: int = 25,
                  db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user),
                  branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(id, Contracts, db)
    return all_contracts_r(search, page, limit, db, branch_id)


@contracts_router.post("/create_contract")
def create_contract(new_contract: CreateContract,
                    db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    create_contract_y(new_contract, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@contracts_router.put("/update_contract")
def update_contract(this_supplier: UpdateContract, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_contract_y(this_supplier, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")