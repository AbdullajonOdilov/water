from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException
from sqlalchemy.orm import Session
from functions.uploaded_func import all_files_r, create_file_e, update_file_e, one_file
from utils.auth import get_current_active_user
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import role_verification

uploaded_router = APIRouter(
    prefix="/uploaded",
    tags=["Uploaded operation"]
)


@uploaded_router.get("/get_uploaded")
def get_files(search: str = None, id: int = 0, page: int = 0, limit: int = 25,
              db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user),
              branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return one_file(id, db)
    return all_files_r(search, page, limit, db,branch_id)


@uploaded_router.post("/create_file")
def create_file(new_file: UploadFile = File(None), source: str = Form(None),
                source_id: int = Form(0), comment: str = Form(None),
                db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    create_file_e(new_file, source=source, db=db, thisuser=current_user, source_id=source_id, comment=comment)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@uploaded_router.put("/update_file")
def update_file(
        id: int = Form(0),
        new_file: UploadFile = File(None), source: str = Form(None),
        source_id: int = Form(0), comment: str = Form(None),
        db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(user=current_user)
    update_file_e(id, new_file, source, source_id, current_user, comment, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


# @uploaded_router.delete("/delete_file")
# def delete_file(id: int, db: Session = Depends(database),
#                 current_user: CreateUser = Depends(get_current_active_user)):
#     role_verification(user=current_user)
#     delete_file_e(id, db)
#     raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")




