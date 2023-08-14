from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.notifications import manager
from functions.user_products_func import create_user_products_y
from models.orders import Orders
from models.products import Products
from models.user_products import User_products
from models.users import Users
from models.warehouse_products import Warehouses_products
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.transfers import Transfers


def all_transfers(status, page, limit, db):
    transfers = db.query(Transfers).options(joinedload(Transfers.order),
                                            joinedload(Transfers.w_product),
                                            joinedload(Transfers.warehouser),
                                            joinedload(Transfers.driver))
    if status==True:
        transfers = transfers.filter(Transfers.status==True)
    if status==False:
        transfers = transfers.filter(Transfers.status == False)
    else:
        transfers = transfers
    transfers = transfers.order_by(Transfers.id.desc())
    return pagination(transfers, page, limit)


def one_transfer(db, ident):
    the_item = db.query(Transfers).filter(Transfers.id == ident).options(joinedload(Transfers.order),
                                            joinedload(Transfers.w_product),
                                            joinedload(Transfers.warehouser),
                                            joinedload(Transfers.driver)).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item


def create_transfers_y(form, db, this_user):
    warehouser = the_one(form.warehouser_id, Users, db)
    if warehouser.role != "warehouser":
        raise HTTPException(status_code=400, detail="bu userni role warehouserga teng emas")
    #product_id ni aniqlash
    w_p = the_one(form.warehouse_product_id, Warehouses_products, db)
    product_id = w_p.product_id
    the_one(form.driver_id, Users, db)
    w_products = db.query(Warehouses_products).filter(Warehouses_products.id == form.warehouse_product_id).first()
    count = w_products.quantity - form.quantity
    if count < 0:
        raise HTTPException(status_code=400, detail='omborda yetarli mahsulot mavjud emas')
    else:
        new_transfers_db = Transfers(
            order_id=form.order_id,
            warehouse_product_id=form.warehouse_product_id,
            quantity=form.quantity,
            date=datetime.now(),
            warehouser_id=this_user.id,
            driver_id=form.driver_id,
            status=False,
        )
        save_in_db(db, new_transfers_db)
        #substraction form warehouse products
        db.query(Warehouses_products).filter(Warehouses_products.id == form.warehouse_product_id).update({
            Warehouses_products.quantity: Warehouses_products.quantity - form.quantity
        })
        db.commit()
        #adding to user products
        create_user_products_y(product_id, form.quantity, db, this_user)


async def update_transfers_y(form, db, this_user):
    users = db.query(Users).filter(Users.status, Users.branch_id == this_user.branch_id).all()
    transfer = the_one(form.id, Transfers, db)
    warehouser = the_one(form.warehouser_id, Users, db)
    # moneyni aniqlash uchun ombordagi productni summasini bilish kerak
    w_p = db.query(Warehouses_products).filter(Warehouses_products.id == transfer.warehouse_product_id).first()
    product = db.query(Products).filter(Products.id == w_p.product_id).first()
    money = form.quantity * product.price
    order = db.query(Orders).filter(Orders.id == transfer.order_id).first()
    if warehouser.role != "warehouser":
        raise HTTPException(status_code=400, detail="bu userni role warehouserga teng emas")
    if order.status > 2:
        raise HTTPException(status_code=400, detail="Bu orderni statusi 2 ga teng")
    if form.status == True:
        db.query(Orders).filter(Orders.id == transfer.order_id).update({
            Orders.status: Orders.status + 1
        })
        db.commit()
    the_one(form.driver_id, Users, db)
    if transfer:
        db.query(Transfers).filter(Transfers.id == form.id).update({
            Transfers.quantity: form.quantity,
            Transfers.date: datetime.now(),
            Transfers.warehouser_id: form.warehouser_id,
            Transfers.driver_id: form.driver_id,
            Transfers.status: form.status
        })
        db.commit()
        # update qilganda agar quantity user_p dagi ham update bo'lishe kerak
        db.query(User_products).filter(User_products.id == form.driver_id).update({
            User_products.quantity: form.quantity
        })
        db.commit()

        db.query(Users).filter(Users.id == form.driver_id, Users.role == 'driver').update({
            Users.balance: Users.balance + money
        })
        db.commit()
        if order.status == 2:
            for user in users:
                data = NotificationSchema(
                    title="Buyurtma muvaffaqiyatli yetkazildi!",
                    body=f"{order.id} dagi buyurtma topshirildi!",
                    user_id=user.id,
                )
                await manager.send_user(message=data, user_id=user.id, db=db)


