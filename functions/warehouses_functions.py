from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.warehouses import Warehouses


def all_warehouses(search, page, limit, db,branch_id):
    warehouses = db.query(Warehouses).join(Warehouses.phones).options(joinedload(Warehouses.phones))
    if branch_id > 0:
        warehouses = warehouses.filter(Warehouses.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses.name.asc())
    return pagination(warehouses, page, limit)


# bitta warehouseni phonesni olish uchun function
def one_warehouse(db, ident):
    the_w = db.query(Warehouses).filter(Warehouses.id == ident).options(joinedload(Warehouses.phones)).first()
    if the_w is None:
        raise HTTPException(status_code=404)
    return the_w

def create_warehouse_e(form, db, thisuser):
    if db.query(Warehouses).filter(Warehouses.address == form.address).first():
                raise HTTPException(status_code=400, detail="Bunday ombor allaqachon bazada bor uni yangilashingiz mumkin")
    new_warehouse_db = Warehouses(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat,
        branch_id=thisuser.branch_id
    )
    save_in_db(db,new_warehouse_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
                    raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
        else:
            number = i.number
            name = i.name
            create_phone(name,comment, number, new_warehouse_db.id, thisuser.id, db, 'warehouses',thisuser.branch_id)


def update_warehouse_e(form, db, thisuser):
    if get_in_db(db, Warehouses, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Warehouse or Phone not found!")

    db.query(Warehouses).filter(Warehouses.id == form.id).update({
        Warehouses.id: form.id,
        Warehouses.name: form.name,
        Warehouses.address: form.address,
        Warehouses.map_lat: form.map_lat,
        Warehouses.map_long: form.map_long,
        Warehouses.branch_id: thisuser.branch_id
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'warehouses',thisuser.branch_id)
