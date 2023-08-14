from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.user_products import User_products
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_user_products(page, limit, branch_id, db):
    products = db.query(User_products).options(joinedload(User_products.this_product),
                                               joinedload(User_products.user))

    if branch_id > 0:
        products = products.filter(User_products.branch_id == branch_id)
    products = products.order_by(User_products.id.desc())
    return pagination(products, page, limit)


def one_user_p(ident, db):
    the_item = db.query(User_products).filter(User_products.id == ident).options(
        joinedload(User_products.this_product),
        joinedload(User_products.user)
    ).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item

def create_user_products_y(product_id, quantity, db, this_user):
    new_user_products_db = User_products(
        product_id=product_id,
        quantity=quantity,
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
