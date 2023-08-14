from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.customer_locations import Customer_locations
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_customer_locations(search, page, limit, db, branch_id):
    customer_locations_query = db.query(Customer_locations).options(joinedload(Customer_locations.customer))
    if branch_id > 0:
        customer_locations_query = customer_locations_query.filter(Customer_locations.branch_id == branch_id)
    if search:
        search_formatted = f"%{search}%"
        customer_locations_query = customer_locations_query.filter(Customer_locations.name.like(search_formatted))
    # Apply order_by to the query object
    customer_locations_query = customer_locations_query.order_by(Customer_locations.id.desc())
    return pagination(customer_locations_query, page, limit)


# bitta customer location  malumotini olish uchun function
def one_customer_l(db, ident):
    the_item = db.query(Customer_locations).filter(Customer_locations.id == ident).options(
        joinedload(Customer_locations.customer)).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item


def create_customer_locations_y(form, db, this_user):
    if db.query(Customer_locations).filter(Customer_locations.map_lat == form.map_lat, Customer_locations.map_long == Customer_locations.map_long).first():
        raise HTTPException(status_code=400, detail="Bu lokatsiya allaqachon bazada bor")
    if db.query(Customer_locations).filter(Customer_locations.address == form.address).first():
        raise HTTPException(status_code=400, detail="Bu adress allaqachon bazada bor")
    new_customer_locations_db = Customer_locations(
        name=form.name,
        map_long=form.map_long,
        map_lat=form.map_lat,
        address=form.address,
        orienter=form.orienter,
        customer_id=form.customer_id,
        user_id=this_user.id,
        branch_id=this_user.branch_id,

    )
    save_in_db(db, new_customer_locations_db)


def update_customer_loactions_y(form, db, this_user):
    if get_in_db(db, Customer_locations, form.id):
        db.query(Customer_locations).filter(Customer_locations.id == form.id).update({
            Customer_locations.name: form.name,
            Customer_locations.map_long: form.map_long,
            Customer_locations.map_lat: form.map_lat,
            Customer_locations.address: form.address,
            Customer_locations.user_id: this_user.id,
            Customer_locations.branch_id: this_user.branch_id,
            Customer_locations.orienter: form.orienter,
            Customer_locations.customer_id: form.customer_id,
        })
        db.commit()


