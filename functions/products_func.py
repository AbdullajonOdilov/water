import os

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.products import Products


def all_products(search, page, limit, db, category_id, branch_id):
    products = db.query(Products).options(joinedload(Products.category))
    if branch_id > 0:
        products = products.filter(Products.branch_id == branch_id)
    if category_id > 0:
        products = products.filter(Products.category_id==category_id)
    if search:
        search_formatted = "%{}%".format(search)
        products = products.filter(Products.name.like(search_formatted))
    products = products.order_by(Products.id.desc())
    return pagination(products, page, limit)


# bitta productni malumotini olish uchun function
def one_product(db, ident):
    the_p = db.query(Products).filter(Products.id == ident).options(joinedload(Products.category)).first()
    if the_p is None:
        raise HTTPException(status_code=404)
    return the_p


def create_products_y(form, db, this_user):
    if db.query(Products).filter(Products.name == form.name).first():
        raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
    else:
        new_products_db = Products(
            name=form.name,
            comment=form.comment,
            price=form.price,
            litr=form.litr,
            category_id=form.category_id,
            user_id=this_user.id,
            branch_id=this_user.branch_id

        )
        save_in_db(db, new_products_db)


def update_products_y(form, db, this_user):
    if the_one(form.id, Products, db):
        db.query(Products).filter(Products.id == form.id).update({
            Products.id: form.id,
            Products.name: form.name,
            Products.comment: form.comment,
            Products.price: form.price,
            Products.litr: form.litr,
            Products.category_id: form.category_id,
            Products.branch_id: this_user.branch_id,
            Products.user_id: this_user.id
        })
        db.commit()



