from fastapi import HTTPException
from models.branches import Branches
from models.orders import Orders
from models.trades import Trades
from models.user_products import User_products
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
    order = the_one(data.order_id, Orders, db)
    warehouse_products = the_one(data.warehouse_pr_id, Warehouses_products, db)
    if db.query(Trades).filter(Trades.order_id == data.order_id).first():
        raise HTTPException(status_code=400, detail="Bunday trade orderga allaqachon allaqachon bazada bor")
    the_one(thisuser.branch_id, Branches, db)

    # Fetch the user_products with the same product_id as warehouse_products
    user_products = db.query(User_products).filter(User_products.product_id == warehouse_products.product_id).first()
    # Now you can access user_products.quantity
    trade_quantity = user_products.quantity - data.quantity
    if trade_quantity < 0:
        raise HTTPException(status_code=400, detail="User productsda yetarli mahsulot yo'q")
    if order.status == 0 or order.status == 1:
        price = warehouse_products.price * data.quantity
        new_trade = Trades(
            warehouse_pr_id=data.warehouse_pr_id,
            price=price,
            quantity=data.quantity, #false,
            order_id=data.order_id,
            user_id=thisuser.id,
            branch_id=thisuser.branch_id
            )
        save_in_db(db, new_trade)
        # user_productsni quantity sini kamaytirish update qilish
        db.query(User_products).filter(User_products.id == user_products.id).update({
            User_products.quantity: User_products.quantity - data.quantity
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Bu order statusi 1 yoki avval order status yangilang yoki yangi order oching")


def update_trade_r(form, db, thisuser):
    the_one(form.id, Trades, db)
    order = the_one(form.order_id, Orders, db)
    warehouse_products = the_one(form.warehouse_pr_id, Warehouses_products, db)
    # Warehouse_products dan product_id ni aniqlab olamiz
    order = the_one(form.order_id, Orders, db)
    user_products = db.query(User_products).filter(User_products.product_id == warehouse_products.product_id).first()
    # User productsdan w_p dagi bir xil product_id ni aniqlaymiz
    trade_quantity = user_products.quantity - form.quantity
    if trade_quantity < 0:
        raise HTTPException(status_code=400, detail="User productsda yetarli mahsulot yo'q")
    if order.status == 0 or order.status == 1:
        price = warehouse_products.price * form.quantity
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
        raise HTTPException(status_code=400, detail="Bu savdo allaqachon bajarilgan, status=3")