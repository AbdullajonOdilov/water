from datetime import datetime

from fastapi import HTTPException

from functions.notifications import manager
from models.orders import Orders
from models.users import Users
from models.warehouse_products import Warehouses_products
from models.warehouses import Warehouses
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.transfers import Transfers


def all_transfers(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Transfers.name.like(search_formatted))
    else:
        search_filter = Transfers.id > 0
    transfers = db.query(Transfers).filter(search_filter).order_by(Transfers.id.desc())
    return pagination(transfers, page, limit)


def create_transfers_y(form, db, this_user):
    warehouser = the_one(form.warehouser_id, Users, db)
    the_one(form.warehouse_product_id, Warehouses_products, db)
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
            warehoueser_id=this_user.id,
            driver_id=form.driver_id,
            status=False,
        )
        save_in_db(db, new_transfers_db)

        db.query(Orders).filter(Orders.id == form.order_id).update({
            Orders.status: Orders.status + 1
        })
        db.commit()

        # db.query(Warehouses_products).filter(Warehouses_products.id == form.warehouse_product_id).update({
        #     Warehouses_products.quantity: Warehouses_products.quantity - form.quantity
        # })
        # db.commit()


async def update_transfers_y(form, db, this_user):
    users = db.query(Users).filter(Users.status, Users.branch_id == this_user.branch_id).all()
    transfer = the_one(form.id, Transfers, db)
    the_one(form.warehouser_id, Users, db)
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

        if form.status == True:
            db.query(Orders).filter(Orders.id == transfer.order_id).update({
                Orders.status: Orders.status + 1
            })
            db.commit()
            order = db.query(Orders).filter(Orders.id == transfer.order_id).first()
            if order.status == 4:
                for user in users:
                    data = NotificationSchema(
                        title="Buyurtma muvaffaqiyatli yetkazildi!",
                        body=f"{order.id} dagi buyurtma topshirildi!",
                        user_id=user.id,
                    )
                    await manager.send_user(message=data, user_id=user.id, db=db)


