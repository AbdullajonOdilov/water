from fastapi import HTTPException
from functions.warehouse_products_func import create_warehouse_products_e
from models.products import Products
from models.supplies import Supplies
from utils.paginatsiya import pagination
from utils.db_operations import save_in_db,get_in_db

def all_supplies_r(search,limit,page,db,branch_id):
    supplies = db.query(Supplies)    
    if search:
        search_formatted = "%{}%".format(search)
        supplies = supplies.filter(Supplies.name.like(search_formatted))
    if branch_id > 0:
        supplies = supplies.filter(Supplies.branch_id == branch_id)
    else:
        supplies = supplies.filter(Supplies.quantity >= 1 )
    if supplies == None or 0:
         raise HTTPException(status_code=404,detail="Bunday parametrga ega supplier  mavjud  emas")
    supplies = supplies.order_by(Supplies.name.asc())
    return pagination(supplies, page, limit)

def create_supplies_r(form,db,this_user):
    if db.query(Supplies).filter(Supplies.name == form.name).first():
            raise HTTPException(status_code=400, detail="Bunday taminotchi allaqachon bazada bor")
    if db.query(Products).filter(Products.id != form.product_id).first():
            raise HTTPException(status_code=404, detail="Bunday product yoq")
    
    new_supplies = Supplies(
        name = form.name,
        product_id = form.product_id,
        quantity=form.quantity,
        price=form.price,
        date=form.date,
        user_id=this_user.id,
        branch_id=this_user.branch_id,
        supplier_id=form.supplier_id
    )
    create_warehouse_products_e(form,db,this_user)
    save_in_db(db,new_supplies)
    # for i in form.phones:
    #     comment = i.comment
    #     if db.query(Phones).filter(Phones.number == i.number).first():
    #                 raise HTTPException(status_code=400, detail="Bu telefon allaqachon bazada bor")
    #     else:
    #         number = i.number
    #         name = i.name
    #         create_phone(name,comment,number,new_supplier.id,this_user.id,db,"supplies",this_user.branch_id)

def update_supplies_r(form,db,this_user):
    if get_in_db(db,Supplies,form.id):
        db.query(Supplies).filter(Supplies.id == form.id).update({
            Supplies.id: form.id,
            Supplies.name: form.name,
            Supplies.product_id: form.product_id,
            Supplies.quantity: form.quantity,
            Supplies.price: form.price,
            Supplies.date: form.date,
            Supplies.user_id: this_user.id,
            Supplies.branch_id: this_user.branch_id,
            Supplies.supplier_id: form.supplier_id
        })
        db.commit()
            
        # for i in form.phones:
        #     phone_id = i.id
        #     comment = i.comment
        #     number = i.number
        #     update_phone(phone_id, comment, number, form.id, this_user.id, db, 'supplies',form.branch_id)