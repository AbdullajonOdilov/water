from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.notifications import manager
from functions.warehouse_products_func import create_warehouse_products_e
from models.products import Products
from models.suppliers import Suppliers
from models.supplies import Supplies
from models.users import Users
from models.warehouses import Warehouses
from schemas.notifications import NotificationSchema
from utils.paginatsiya import pagination
from utils.db_operations import save_in_db, the_one


def all_supplies_r(search, limit, page, db, branch_id):
    supplies = db.query(Supplies).options(joinedload(Supplies.warehouse), joinedload(Supplies.product))
    if search:
        search_formatted = "%{}%".format(search)
        supplies = supplies.filter(Supplies.name.like(search_formatted))
    if branch_id > 0:
        supplies = supplies.filter(Supplies.branch_id == branch_id)
    else:
        supplies = supplies.filter(Supplies.quantity >= 1)
    if supplies == None or 0:
         raise HTTPException(status_code=404, detail="Bunday parametrga ega supplier  mavjud  emas")
    supplies = supplies.order_by(Supplies.id.desc())
    return pagination(supplies, page, limit)


async def create_supplies_r(form, db, this_user):
    users = db.query(Users).filter(Users.role == 'admin', Users.role == 'branch_admin').all()
    the_one(form.product_id, Products, db)
    the_one(form.warehouse_id, Warehouses, db)
    the_one(form.supplier_id, Suppliers, db)
    new_supplies = Supplies(
        warehouse_id=form.warehouse_id,
        product_id=form.product_id,
        quantity=form.quantity,
        price=form.price,
        date=datetime.now(),
        user_id=this_user.id,
        branch_id=this_user.branch_id,
        supplier_id=form.supplier_id
    )
    create_warehouse_products_e(form, db, this_user)
    save_in_db(db, new_supplies)
    if new_supplies:
        for user in users:
            data = NotificationSchema(
                title="Yangi ta'minot yaratildi!",
                body=f"{this_user.id.name} ismli user yangi taminotni qoshdi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)


async def update_supplies_r(form, db, this_user):
    users = db.query(Users).filter(Users.role == 'admin', Users.role == 'branch_admin').all()
    the_one(form.supplier_id, Suppliers, db), the_one(form.product_id, Products, db)
    if the_one(form.id, Supplies, db):
        supply = db.query(Supplies).filter(Supplies.id == form.id).update({
            Supplies.product_id: form.product_id,
            Supplies.quantity: form.quantity,
            Supplies.price: form.price,
            Supplies.date: datetime.now(),
            Supplies.user_id: this_user.id,
            Supplies.branch_id: this_user.branch_id,
            Supplies.supplier_id: form.supplier_id
        })
        db.commit()

        if supply:
            for user in users:
                data = NotificationSchema(
                    title="Ta'minot o'zgartirildi!",
                    body=f"{this_user.id.name} ismli user ta'minotga o'zgartirish kiritdi!",
                    user_id=user.id,
                )

                await manager.send_user(message=data, user_id=user.id, db=db)
