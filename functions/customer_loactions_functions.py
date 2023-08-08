from fastapi import HTTPException
from models.customer_locations import Customer_locations
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_customer_locations(search, page, limit, db,branch_id):
    customer_locations = db.query(Customer_locations)
    if branch_id > 0:
        customer_locations = db.query(Customer_locations).filter(Customer_locations.branch_id == branch_id)
    if search :
        search_formatted = "%{}%".format(search)
        customer_locations = customer_locations.filter(Customer_locations.name.like(search_formatted))
    else :
        search_filter = Customer_locations.id > 0
    customer_locations = customer_locations.filter(search_filter).order_by(Customer_locations.name.asc())
    return pagination(customer_locations, page, limit)


def create_customer_locations_y(form, db, this_user):
    if db.query(Customer_locations).filter(Customer_locations.map_lat == form.map_lat).first():
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


