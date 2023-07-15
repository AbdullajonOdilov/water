import os
from fastapi import HTTPException
from models.supplies import Supplies
from models.branches import Branches
from models.customers import Customers
from models.warehouse_products import Warehouses
from models.uploaded_files import Uploaded
from models.users import Users
from utils.db_operations import save_in_db
from utils.paginatsiya import pagination

def all_files_r(search, page, limit, db,branch_id):
    uploaded = db.query(Uploaded)
    if branch_id > 0:
        uploaded = uploaded.filter(Uploaded.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = uploaded.filter(Uploaded.comment.like(search_formatted))
    else :
        search_filter = Uploaded.id > 0
    uploaded = uploaded.filter(search_filter).order_by(Uploaded.source.asc())
    return pagination(uploaded, page, limit)

def create_file_e(new_file, source, source_id, db, thisuser,comment,branch_id):
    if db.query(Uploaded).filter(Uploaded.source == source,
                                       Uploaded.source_id == source_id).first():
        raise HTTPException(status_code=400, detail="This source already have his own file!")
    if (db.query(Users).filter(Users.id == source_id).first() and source == "user") or \
       (db.query(Branches).filter(Branches.id == source_id).first() and source == "branch") or \
       (db.query(Supplies).filter(Supplies.id == source_id).first() and source == "supplies") or \
       (db.query(Customers).filter(Customers.id == source_id).first() and source == "customers") or \
       (db.query(Warehouses).filter(Warehouses.id == source_id).first() and source == "warehouses"):
        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"Uploaded/{new_file.filename}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        new_file_db = Uploaded(
            file=new_file.filename,
            comment=comment,
            source=source,
            source_id=source_id,
            user_id=thisuser.id,
            branch_id=branch_id
        )
        save_in_db(db, new_file_db)
    else:
        raise HTTPException(status_code=400, detail="Source error!")


def update_file_e(id, new_file, source, source_id, db, user,comment):
    # the_one(db, Uploaded, id, user)
    this_file = db.query(Uploaded).filter(Uploaded.source == source,
                                                Uploaded.source_id == source_id).first()
    if this_file and this_file.id != id:
        raise HTTPException(status_code=400,
                            detail="Siz kiritayotgan idli file ushbu sourcega tegishli "
                                   "emas va siz kiritayotgan sourcening ozini fayli bor")
    if (db.query(Users).filter(Users.id == source_id).first() and source == "user") or \
       (db.query(Branches).filter(Branches.id == source_id).first() and source == "branch") or \
       (db.query(Supplies).filter(Supplies.id == source_id).first() and source == "supplies") or \
       (db.query(Customers).filter(Customers.id == source_id).first() and source == "customers") or \
       (db.query(Warehouses).filter(Warehouses.id == source_id).first() and source == "warehouses"):
        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"Uploaded/{file_location}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        db.query(Uploaded).filter(Uploaded.id == id).update({
            Uploaded.id: id,
            Uploaded.file: new_file.filename,
            Uploaded.comment: comment,
            Uploaded.source: source,
            Uploaded.source_id: source_id,
            Uploaded.user_id: user.id,
            Uploaded.branch_id: user.branch_id
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Source error!")


# def delete_file_e(id, db, user):
#     file = the_one(db, Uploaded, id, user)
#     if file.source == "collaction" or file.source == "material" or file.source == "mechanism":
#         raise HTTPException(status_code=400, detail="Userdan boshqasini rasmini ochirib bolmaydi!")
#     db.query(Uploaded).filter(Uploaded.id == id).delete()
#     db.commit()