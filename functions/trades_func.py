from fastapi import HTTPException
from models.branches import Branches
from models.orders import Orders
from models.trades import Trades
from models.warehouse_products import Warehouses_products
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination
from sqlalchemy.orm import joinedload,join

def all_trades_r(search, page, limit, db,branch_id):
    trades = db.query(Trades).join(Trades.order).options(joinedload(Trades.order))
    if branch_id > 0:
        trades = trades.filter(Trades.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        trades = trades.filter(Trades.name.like(search_formatted))
    trades = trades.order_by(Trades.name.asc())
    return pagination(trades, page, limit)


def create_trade_r(data, db, thisuser):
    # if db.query(Trades).filter(Trades.order_id == data.order_id).first():
    #             raise HTTPException(status_code=400, detail="Bunday trade orderga allaqachon allaqachon bazada bor")
    order = get_in_db(db, Orders, data.order_id)
    if order.status  == "0" and get_in_db(db,Warehouses_products,data.warehouse_pr_id) != None and get_in_db(db,Branches,thisuser.branch_id) != None:
        product = db.query(Warehouses_products).filter(Warehouses_products.id == data.warehouse_pr_id).first()
        new_product_quantity = product.quantity - data.quantity
        price = product.price * data.quantity
        if new_product_quantity >= 0:
            new_trade = Trades(
                name=data.name,
                warehouse_pr_id=data.warehouse_pr_id,
                price=price,
                quantity=data.quantity,#false,
                order_id=data.order_id,
                user_id=thisuser.id,
                branch_id=thisuser.branch_id

            )
            save_in_db(db, new_trade)
            db.query(Warehouses_products).filter(Warehouses_products.id == data.warehouse_pr_id).update({
            Warehouses_products.quantity: new_product_quantity
        })
            db.commit()
            # kassa = db.query(Kassas).filter(Kassas.branch_id == data.branch_id).first()
            # create_income_r("trade",data.order_id,kassa.id,thisuser.id,"TRade Income","trade",price,data.branch_id,db)
        else:
             raise HTTPException(status_code=400,detail="Warehouse da buncha maxsulot mavjud emas")
    else:
        raise HTTPException(status_code=400,detail="Bu order statusi 1 yoki avval order status yangilang yoki yangi order oching")
