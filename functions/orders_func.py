from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.notifications import manager
from models.branches import Branches
from models.customer_locations import Customer_locations
from models.customers import Customers
from models.users import Users
from models.warehouses import Warehouses
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, get_in_db, the_one
from utils.paginatsiya import pagination
from models.orders import Orders


def all_orders(search, page, limit, db,branch_id):
    orders = db.query(Orders).join(Orders.customer_loc).join(Orders.created_user).options(joinedload(Orders.customer_loc), joinedload(Orders.created_user))
    if branch_id > 0:
        orders = orders.filter(Orders.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(Users.name.like(search_formatted) | Users.username.like(search_formatted) | Customers.name.like(search_formatted))
    orders = orders.order_by(Orders.id.desc())
    return pagination(orders, page, limit)


# bitta order malumotini olish uchun function
def one_order(db, ident):
    the_p = db.query(Orders).filter(Orders.id == ident).options(joinedload(Orders.this_operator),
                                                                joinedload(Orders.this_driver),
                                                                joinedload(Orders.this_warehouser),
                                                                joinedload(Orders.customer_loc)).first()
    if the_p is None:
        raise HTTPException(status_code=404)
    return the_p


async def create_order_r(data, db, thisuser):
    users = db.query(Users).filter(Users.status, Users.branch_id == thisuser.branch_id).all()
    the_one(data.customer_loc_id, Customer_locations, db)
    branch = db.query(Branches).filter(Branches.id == thisuser.branch_id).first()
    old_number = len(db.query(Orders).all())
    print(old_number)
    customer_address = db.query(Customer_locations).filter(Customer_locations.id == data.customer_loc_id).first()
    if branch:
        new_order = Orders(
            operator_id=thisuser.id,
            status=0,
            driver_id=0,
            date=datetime.now(),
            warehouser_id=0,
            customer_loc_id=data.customer_loc_id,
            user_id=thisuser.id,
            branch_id=thisuser.branch_id,
            number=old_number + 1
        )
        save_in_db(db, new_order)

        if new_order.status == 0:
            for user in users:
                notification_data = NotificationSchema(
                    title="Yangi buyurtma yaratildi!",
                    body=f"Diqqat {customer_address.name} shu address bo'yicha buyurtma olindi!",
                    user_id=user.id
                )
                await manager.send_user(message=notification_data, user_id=user.id, db=db)


async def update_order_r(data, db, thisuser):
    users = db.query(Users).filter(Users.status, Users.branch_id == thisuser.branch_id).all()
    the_one(data.customer_loc_id, Customer_locations, db)
    the_one(data.driver_id, Users, db)
    the_one(data.warehouser_id, Users, db)
    order = the_one(data.id, Orders, db)
    if db.query(Orders).filter(Orders.id == data.id).first().status == 2:
        raise HTTPException(status_code=400, detail=f"Bu id: {data.id} dagi order  bajarildi!")
    if db.query(Orders).filter(Orders.id == data.id).first().status == 0 and data.status != 0 and data.status != 1:
        raise HTTPException(status_code=400, detail="Bu order statusi 0 ga yani false ga teng siz "
                                                    "xozir buni faqat 0 yoki 1 yani bajarilmoqda ga ozgartirishingiz mumkin")
    if db.query(Orders).filter(Orders.id == data.id).first().status == 1 and data.status != 0 and data.status != 1 and data.status != 2:
        raise HTTPException(status_code=400,
                            detail="Bu order xozir 1 yani bajarilmoqdaga teng uni 0 yoki 1 ligicha "
                                   "yoki 2 bajarildi ga ozgartirishingiz mumkin")
    db.query(Orders).filter(Orders.id == data.id).update({
        Orders.operator_id: thisuser.id,
        Orders.driver_id: data.driver_id,
        Orders.warehouser_id: data.warehouser_id,
        Orders.customer_loc_id: data.customer_loc_id,
        Orders.date: datetime.now(),
        Orders.branch_id: thisuser.branch_id,
        Orders.user_id: thisuser.id,
        Orders.status: data.status
    })
    db.commit()
    user_id = db.query(Users).filter(Users.id == data.driver_id).first()
    if order.status == 1:
        for user in users:
            data = NotificationSchema(
                title="Buyurtma haydovchiga biriktirildi!",
                body=f"Hurmatli foydalanuvchi {user_id.name} buyurtma sizga biriktirildi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)


def delete_order_r(id, db):
    the_one(id, Orders, db)
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()










