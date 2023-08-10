from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.products import Products
from models.warehouses import Warehouses
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.warehouse_products import Warehouses_products


def all_warehouses_products(search, page, limit, db, branch_id, warehouse_id):
    warehouses = db.query(Warehouses_products).options(joinedload(Warehouses_products.product))
    if warehouse_id > 0:
        warehouses = warehouses.filter(Warehouses_products.warehouse_id == warehouse_id)
    if branch_id > 0:
        warehouses = warehouses.filter(Warehouses_products.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses_products.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses_products.id.desc())
    return pagination(warehouses, page, limit)


def create_warehouse_products_e(form, db, thisuser):
    the_one(form.product_id, Products, db)
    the_one(form.warehouse_id, Warehouses, db)
    new_warehouse_db = Warehouses_products(
        product_id=form.product_id,
        quantity=form.quantity,
        price=form.price,
        warehouse_id=form.warehouse_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_warehouse_db)


def update_warehouse_products_e(form, db, thisuser):
    the_one(form.product_id, Products, db)
    the_one(form.warehouse_id, Warehouses, db)
    if the_one(form.id, Warehouses_products, db):
        db.query(Warehouses_products).filter(Warehouses_products.id == form.id).update({
            Warehouses_products.product_id: form.product_id,
            Warehouses_products.quantity: form.quantity,
            Warehouses_products.price: form.price,
            Warehouses_products.warehouse_id: form.warehouse_id,
            Warehouses_products.branch_id: thisuser.branch_id
        })
        db.commit()
    else: 
        raise HTTPException(status_code=400, detail="Warehouse products topilmadi")





