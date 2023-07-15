from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.warehouse_products import Warehouses_products


def all_warehouses_products(search, page, limit, db,branch_id):
    warehouses = db.query(Warehouses_products)
    if branch_id > 0:
        warehouses = warehouses.filter(Warehouses_products.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses_products.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses_products.name.asc())
    return pagination(warehouses, page, limit)


def create_warehouse_products_e(form, db, thisuser):
    # if db.query(Warehouses_products).filter(Warehouses_products.product_id == form.product_id).first():
    #             update_warehouse_products_e(form, db, thisuser)
    #             raise HTTPException(status_code=201, detail="Bunday product dan avval omborda bo'lganligi sababli uni yangiladik")
    new_warehouse_db = Warehouses_products(
        name=form.name,
        product_id=form.product_id,
        quantity=form.quantity,
        price=form.price,
        warehouse_id = form.warehouse_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db,new_warehouse_db)
    # for i in form.phones:
    #     comment = i.comment
    #     if db.query(Phones).filter(Phones.number == i.number).first():
    #                 raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
    #     else:
    #         number = i.number
    #         name = i.name
    #         create_phone(name,comment, number, new_warehouse_db.id, thisuser.id, db, 'warehouses',thisuser.branch_id)


def update_warehouse_products_e(form, db, thisuser):
    if get_in_db(db, Warehouses_products, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Warehouse or Phone not found!")

    db.query(Warehouses_products).filter(Warehouses_products.id == form.id).update({
        Warehouses_products.id: form.id,
        Warehouses_products.name: form.name,
        Warehouses_products.product_id: form.product_id,
        Warehouses_products.quantity: form.quantity,
        Warehouses_products.price: form.price,
        Warehouses_products.warehouse_id: form.warehouse_id,
        Warehouses_products.branch_id: thisuser.branch_id
    })
    db.commit()

    # for i in form.phones:
    #     phone_id = i.id
    #     comment = i.comment
    #     number = i.number
    #     update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'warehouses',form.branch_id)






