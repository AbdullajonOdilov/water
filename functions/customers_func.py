from fastapi import HTTPException
from functions.phones_func import create_phone, update_phone
from models.customer_locations import Customer_locations
from models.customers import Customers
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from sqlalchemy.orm import joinedload


def all_customers(search, page, limit, db,branch_id):
    customers = db.query(Customers).join(Customers.phones).join(Customers.customer_loc).options(joinedload(Customers.phones),joinedload(Customers.customer_loc))
    if branch_id > 0:
        customers = customers.filter(Customers.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(Customers.name.like(search_formatted))
    else:
        search_filter = Customers.id > 0
    customers = customers.filter(search_filter).order_by(Customers.name.asc())
    return pagination(customers, page, limit)


def create_customers_y(form, db, this_user):
    if db.query(Customers).filter(Customers.name == form.name).first():
        raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
    if form.type not in ['premium', 'umumiy']:
        raise HTTPException(status_code=400, detail="Type error")
    else:
        new_customers_db = Customers(
            name=form.name,
            type=form.type,
            comment=form.comment,
            user_id=this_user.id,
            branch_id=this_user.branch_id,
            balance=form.balance

        )
        save_in_db(db, new_customers_db)
        for i in form.phones:
            comment = i.comment
            if db.query(Phones).filter(Phones.number == i.number).first():
                raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
            else:
                name = i.name
                number = i.number
                create_phone(name,comment,number,new_customers_db.id,this_user.id,db,"customers",this_user.branch_id)
        raise HTTPException(status_code=200,detail=new_customers_db.id)


def update_customers_y(form, db, this_user):
    if form.type not in ['premium', 'umumiy']:
        raise HTTPException(status_code=400, detail="Type error")
    if the_one(form.id, Customers, db):
        db.query(Customers).filter(Customers.id == form.id).update({
            Customers.name: form.name,
            Customers.type: form.type,
            Customers.comment: form.comment,
            Customers.user_id: this_user.id,
            Customers.branch_id: this_user.branch_id,
            Customers.balance: form.balance
        })
        db.commit()
        
        for i in form.phones:
            phone_id = i.id
            comment = i.comment
            number = i.number
            update_phone(phone_id, comment, number, form.id, this_user.id, db, 'customers',this_user.branch_id)


