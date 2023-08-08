from datetime import datetime

from functions.notifications import manager
from models.orders import Orders
from models.users import Users
from models.warehouses import Warehouses
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.transfers import Transfers


def all_transfers(search, page, limit, db):
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Transfers.name.like(search_formatted))
    else:
        search_filter = Transfers.id > 0
    transfers = db.query(Transfers).filter(search_filter).order_by(Transfers.id.desc())
    return pagination(transfers, page, limit)


async def create_transfers_y(form, db, this_user):
    the_one(form.warehoueser_id, Warehouses, db)
    the_one(form.driver_id, Users, db)
    new_transfers_db = Transfers(
        order_id=form.order_id,
        warehouse_product_id=form.warehouse_product_id,
        quantity=form.quantity,
        date=datetime.now(),
        warehoueser_id=form.warehoueser_id,
        driver_id=form.driver_id,
        status=form.status
    )
    save_in_db(db, new_transfers_db)

    db.query(Orders).filter(Orders.id == form.order_id).update({
        Orders.status: Orders.status + 1
    })
    db.commit()


async def update_transfers_y(form, db, this_user):
    users = db.query(Users).filter(Users.status, Users.branch_id == this_user.branch_id).all()
    transfer = the_one(form.id, Transfers, db)
    the_one(form.warehoueser_id, Warehouses, db)
    the_one(form.driver_id, Users, db)
    if transfer:
        db.query(Transfers).filter(Transfers.id == form.id).update({
            Transfers.quantity: form.quantity,
            Transfers.date: datetime.now(),
            Transfers.warehoueser_id: form.warehoueser_id,
            Transfers.driver_id: form.driver_id,
            Transfers.status: form.status
        })
        db.commit()

        if form.status == True:
            order = db.query(Orders).filter(Orders.id == transfer.order_id).update({
                Orders.status: Orders.status + 1
            })
            db.commit()

            if order.status == 3:
                for user in users:
                    data = NotificationSchema(
                        title="Buyurtma muvaffaqiyatli yetkazildi!",
                        body=f"{order.id} dagi buyurtma topshirildi!",
                        user_id=user.id,
                    )
                    await manager.send_user(message=data, user_id=user.id, db=db)


