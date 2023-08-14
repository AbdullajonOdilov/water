from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.branches import Branches


def all_branches(search, page, limit, status, db):
    branches = db.query(Branches)
    if search:
        branches = branches.filter(Branches.name.ilike(f"%{search}%"))
    if status is True:
        branches = branches.filter(Branches.status == True)
    elif status is False:
        branches = branches.filter(Branches.status == False)
    else:
        branches = branches
    branches = branches.order_by(Branches.id.desc())
    return pagination(branches, page, limit)


def create_branch_r(form, db, thisuser):
    if db.query(Branches).filter(Branches.name == form.name).first():
        raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
    if db.query(Branches).filter(Branches.address == form.address).first():
        raise HTTPException(status_code=400, detail="Bunday adress allaqachon bazada bor")
    if thisuser.role in ["admin", "branch_admin"]:
        new_branche_db = Branches(
                name=form.name,
                address=form.address,
                map_lat=form.map_lat,
                map_long=form.map_long,
                status=form.status
            )
        save_in_db(db, new_branche_db)
    else:
        raise HTTPException(status_code=400, detail='Sizga ruxsat berilmagan!')

    for i in form.phones:
            comment = i.comment
            if db.query(Phones).filter(Phones.number == i.number).first():
                raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
            else:
                name = i.name
                number = i.number
                create_phone(name, comment, number, new_branche_db.id, thisuser.id, db, "branch",  thisuser.branch_id)
                

def update_branch_r(form, db, thisuser):
    if get_in_db(db, Branches, form.id) is None or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Branch or Phone not found!")
    if thisuser.role in ["admin", "branch_admin"]:
        db.query(Branches).filter(Branches.id == form.id).update({
            Branches.id: form.id,
            Branches.name: form.name,
            Branches.address: form.address,
            Branches.map_long: form.map_long,
            Branches.map_lat: form.map_lat,
            Branches.status: form.status
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail='Sizga ruxsat berilmagan!')

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'branch',form.id or None)



