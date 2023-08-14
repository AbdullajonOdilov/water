from fastapi import HTTPException

from models.customer_locations import Customer_locations
from models.products import Products
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.customer_loc_pro import Customer_loc_products
from sqlalchemy.orm import joinedload


def all_customer_loc_products(page, limit, db, branch_id):
    customer_loc_products = db.query(Customer_loc_products).options(joinedload(Customer_loc_products.customer_loc),
                                                                    joinedload(Customer_loc_products.product))
    if branch_id > 0:
        customer_loc_products = customer_loc_products.filter(Customer_loc_products.branch_id == branch_id)
    customer_loc_products = customer_loc_products.order_by(Customer_loc_products.id.desc())
    return pagination(customer_loc_products, page, limit)


# bitta customer location product malumotini olish uchun function
def one_clp(db, ident):
    the_item = db.query(Customer_loc_products).filter(Customer_loc_products.id == ident).options(
        joinedload(Customer_loc_products.customer_loc), joinedload(Customer_loc_products.product)).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item


def create_customer_loc_product_y(form, db, this_user):
    the_one(form.customer_loc_id, Customer_locations, db)
    the_one(form.product_id, Products, db)
    new_customer_loc_product = Customer_loc_products(
        customer_loc_id=form.customer_loc_id,
        quantity=form.quantity,
        product_id=form.product_id,
        user_id=this_user.id,
        branch_id=this_user.branch_id
    )
    save_in_db(db, new_customer_loc_product)


def update_customer_loc_product_y(form, db, this_user):
    the_one(form.id, Customer_loc_products, db)
    the_one(form.customer_loc_id, Customer_locations, db)
    the_one(form.product_id, Products, db)
    db.query(Customer_loc_products).filter(Customer_loc_products.id == form.id).update({
        Customer_loc_products.quantity: form.quantity,
        Customer_loc_products.product_id: form.product_id,
        Customer_loc_products.user_id: this_user.id
    })
    db.commit()

