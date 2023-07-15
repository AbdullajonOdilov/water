from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.suppliers import Suppliers

def all_suppliers(search, page, limit, db,branch_id):
    suppliers = db.query(Suppliers).join(Suppliers.phones).options(joinedload(Suppliers.phones))
    if branch_id > 0:
        suppliers = suppliers.filter(Suppliers.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        suppliers = suppliers.filter(Suppliers.name.like(search_formatted))
    suppliers = suppliers.order_by(Suppliers.name.asc())
    return pagination(suppliers, page, limit)


def create_supplier_e(form, db, thisuser):
    if db.query(Suppliers).filter(Suppliers.address == form.address).first():
                raise HTTPException(status_code=400, detail="Bunday supplier allaqachon bazada bor uni yangilashingiz mumkin")
    new_supplier_db = Suppliers(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat,
        branch_id=thisuser.branch_id,
        user_id=thisuser.id
    )
    save_in_db(db,new_supplier_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
                    raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
        else:
            number = i.number
            name = i.name
            create_phone(name,comment, number, new_supplier_db.id, thisuser.id, db, 'suppliers',thisuser.branch_id)


def update_supplier_e(form, db, thisuser):
    if get_in_db(db, Suppliers, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Supplier or Phone not found!")

    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.id: form.id,
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.map_lat: form.map_lat,
        Suppliers.map_long: form.map_long,
        Suppliers.branch_id: thisuser.branch_id,
        Suppliers.user_id: thisuser.id
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'suppliers',thisuser.branch_id)
