from fastapi import APIRouter, Body, HTTPException, Depends, UploadFile,Form
from sqlalchemy.orm import Session
from functions.products_func import all_products,create_products_y,update_products_y
from functions.uploaded_func import all_files_r, create_file_e, update_file_e
from models.products import Products
from utils.auth import get_current_user
from schemas.uploaded_schemas import CreateUpload, UpdateUpload
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from schemas.products_schemas import CreateProducts,UpdateProducts
from db import database
from utils.role_checker import *

uploaded_router = APIRouter(
    prefix="/uploaded",
    tags=["Uploaded operation"]
)


@uploaded_router.get("/get_uploaded")
def get_files(search: str = None, id: int = 0, page: int = 0, limit: int = 25,db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user),branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Products, id)
    return all_files_r(search, page, limit, db,branch_id)


@uploaded_router.post("/create_file")
def create_file(new_file: UploadFile, source: str=Form("branch"),
                source_id: int = Form(1), comment: str = Form("XI"),
                branch_id: int = Form(1), db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    if source == "branch":
        create_file_e(new_file,source=source, db=db, thisuser=current_user, source_id=source_id,comment=comment,branch_id=branch_id)
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
    else:
        raise HTTPException(status_code=404, detail="notogri malumot kiritdingiz")


@uploaded_router.put("/update_file")
def update_file(this_file: CreateUpload, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_file_e(this_file.id, this_file.file, this_file.source,
                  this_file.source_id, db, current_user, this_file.comment)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






