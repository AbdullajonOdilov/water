from models.user_products import User_products
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_user_products(page, limit, db, branch_id):
    products = db.query(User_products)
    if branch_id > 0:
        products = products.filter(User_products.branch_id == branch_id)
    products = products.order_by(User_products.name.asc())
    return pagination(products, page, limit)


def create_user_products_y(form, db,this_user):
    new_user_products_db = User_products(
        product_id=form.product_id,
        quantity=form.quantity,
        user_id=this_user.id,
        branch_id=this_user.branch_id
    )
    save_in_db(db, new_user_products_db)


def update_user_products_y(form,db,this_user):
    if get_in_db(db, User_products, form.id):
        db.query(User_products).filter(User_products.id == form.id).update({
            User_products.product_id: form.product_id,
            User_products.quantity: form.quantity,
            User_products.user_id: this_user.id,
            User_products.branch_id: this_user.branch_id
        })
        db.commit()
