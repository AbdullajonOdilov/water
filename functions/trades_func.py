from fastapi import HTTPException
from models.branches import Branches
from models.orders import Orders
from models.trades import Trades
from models.warehouse_products import Warehouses_products
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from sqlalchemy.orm import joinedload, join


def all_trades_r(search, page, limit, db, branch_id):
    trades = db.query(Trades).options(joinedload(Trades.order))
    if branch_id > 0:
        trades = trades.filter(Trades.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        trades = trades.filter(Trades.name.like(search_formatted))
    trades = trades.order_by(Trades.id.desc())
    return pagination(trades, page, limit)


def create_trade_r(data, db, thisuser):
    if db.query(Trades).filter(Trades.order_id == data.order_id).first():
        raise HTTPException(status_code=400, detail="Bunday trade orderga allaqachon allaqachon bazada bor")
    the_one(thisuser.branch_id, Branches, db)
    the_one(data.warehouse_pr_id, Warehouses_products, db)
    order = the_one(data.order_id, Orders, db)
    if order.status == 0 or order.status == 1:
        product = db.query(Warehouses_products).filter(Warehouses_products.id == data.warehouse_pr_id).first()
        new_product_quantity = product.quantity - data.quantity
        price = product.price * data.quantity
        if new_product_quantity >= 0:
            new_trade = Trades(
                warehouse_pr_id=data.warehouse_pr_id,
                price=price,
                quantity=data.quantity, #false,
                order_id=data.order_id,
                user_id=thisuser.id,
                branch_id=thisuser.branch_id

            )
            save_in_db(db, new_trade)

            db.commit()
            # kassa = db.query(Kassas).filter(Kassas.branch_id == data.branch_id).first()
            # create_income_r("trade",data.order_id,kassa.id,thisuser.id,"TRade Income","trade",price,data.branch_id,db)
        else:
             raise HTTPException(status_code=400, detail="Warehouse da buncha maxsulot mavjud emas")
        db.query(Orders).filter(Orders.id == data.order_id).update({
            Orders.status: Orders.status + 1
        })
    else:
        raise HTTPException(status_code=400, detail="Bu order statusi 1 yoki avval order status yangilang yoki yangi order oching")


def update_trade_r(form, db, thisuser):
    order = the_one(form.order_id, Orders, db)
    product = db.query(Warehouses_products).filter(Warehouses_products.id == form.warehouse_pr_id).first()
    # new_quantity = trade.quantity + form.quantity
    price = product.price * form.quantity
    if order.status != 4:
        if the_one(form.id, Trades, db):
            db.query(Trades).filter(Trades.id == form.id).update({
                Trades.warehouse_pr_id: form.warehouse_pr_id,
                Trades.quantity: form.quantity,
                Trades.price: price,
                Trades.order_id: order.id,
                Trades.user_id: thisuser.id,
                Trades.branch_id: thisuser.branch_id
            })
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Trade topilmadi")
    else:
        raise HTTPException(status_code=400, detail="Bu savdo allaqachon bajarilgan, status=3")