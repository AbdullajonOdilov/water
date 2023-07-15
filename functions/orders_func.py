from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.branches import Branches
from models.customer_locations import Customer_locations
from models.customers import Customers
from models.users import Users
from utils.db_operations import save_in_db,get_in_db
from utils.paginatsiya import pagination
from models.orders import Orders
from utils.role_checker import role_admin, role_driver, role_operator, role_warehouser


def all_orders(search, page, limit, db,branch_id):
    orders = db.query(Orders).join(Orders.customer_loc).join(Orders.created_user).join(Orders.trades).options(joinedload(Orders.customer_loc), joinedload(Orders.created_user), joinedload(Orders.trades))
    if branch_id > 0:
        orders = orders.filter(Orders.branch_id ==  branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(Users.name.like(search_formatted) | Users.username.like(search_formatted) | Customers.name.like(search_formatted))
    orders = orders.order_by(Orders.status.asc())
    return pagination(orders, page, limit)


def create_order_r(data, db, thisuser):
    get_in_db(db, Customer_locations, data.customer_loc_id)
    driver = db.query(Users).filter(Users.id == data.driver_id).first()
    warehouser = db.query(Users).filter(Users.id == data.warehouser_id).first()
    branch = db.query(Branches).filter(Branches.id == thisuser.branch_id).first()
    operator = db.query(Users).filter(Users.id == thisuser.id).first()
    if role_admin(thisuser) or role_warehouser(warehouser) or role_driver(driver) or role_operator(operator) or branch != None:
        new_order = Orders(
            name = data.name,
            operator_id=thisuser.id,
            status="0",#false,
            driver_id=data.driver_id,
            warehouser_id=data.warehouser_id,
            orienter=data.orienter,
            customer_loc_id=data.customer_loc_id,
            user_id=thisuser.id,
            branch_id=thisuser.branch_id,
        )
        save_in_db(db, new_order)


def update_order_r(data, db, thisuser):
    get_in_db(db, Orders, data.id)
    if db.query(Orders).filter(Orders.id == data.id).first().status == "2":
        raise HTTPException(status_code=400, detail=f"Bu id: {data.id} dagi order  bajarildi!")
    if db.query(Orders).filter(Orders.id == data.id).first().status == "0" and data.status != "0" and data.status != "1":
        raise HTTPException(status_code=400, detail="Bu order statusi 0 ga yani false ga teng siz xozir buni faqat 0 yoki 1 yani bajarilmoqda ga ozgartirishingiz mumkin")
    if db.query(Orders).filter(Orders.id == data.id).first().status == "1" and data.status != "0" and data.status != "1" and data.status != "2":
        raise HTTPException(status_code=400,
                            detail="Bu order xozir 1 yani bajarilmoqdaga teng uni 0 yoki 1ligicha yoki 2 bajarildi ga ozgartirishingiz mumkin")
    db.query(Orders).filter(Orders.id == data.id).update({
        Orders.id: data.id,
        Orders.name: data.name,
        Orders.operator_id: thisuser.id,
        Orders.driver_id: data.driver_id,
        Orders.warehouser_id: data.warehouser_id,
        Orders.orienter: data.orienter,
        Orders.customer_loc_id: data.customer_loc_id,
        Orders.branch_id: thisuser.branch_id,
        Orders.user_id: thisuser.id,
        Orders.status: data.status
    })
    db.commit()


def delete_order_r(id, db):
    get_in_db(db, Orders, id)
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()







