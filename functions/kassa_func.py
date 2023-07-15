from functions.phones_func import create_phone
from models.branches import Branches
from models.kassa import Kassas
from models.users import Users
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination
from sqlalchemy.orm import joinedload


def all_kassa_r(search, page, limit, db,branch_id):
    kassa = db.query(Kassas).join(Kassas.phones).options(joinedload(Kassas.phones))
    if branch_id > 0:
        kassa = kassa.filter(Kassas.branch_id == branch_id)
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Kassas.name.like(search_formatted))
    else :
        search_filter = Kassas.id > 0
    kassa = kassa.filter(search_filter).order_by(Kassas.name.asc())
    return pagination(kassa, page, limit)

def create_kassa_r(data, db, thisuser):
    user = get_in_db(db, Users, thisuser.id)
    branch = get_in_db(db,Branches,data.branch_id)
    if user and branch:
        new_kassa = Kassas(
            name=data.name,
            comment=data.comment,
            balance=data.balance,
            user_id=thisuser.id,
            branch_id=thisuser.branch_id

        )
        save_in_db(db, new_kassa)
        for i in data.phones:
            name = i.name
            comment = i.comment
            number = i.number
            create_phone(name,comment,number,new_kassa.id,thisuser.id,db,"kassa",thisuser.branch_id)
def update_kassa_r(id,money,db,user_id):
    old_balance = db.query(Kassas).filter(Kassas.id == id).first()
    new_balance = old_balance.balance + money
    db.query(Kassas).filter(Kassas.id == id).update({
        Kassas.balance: new_balance,
        Kassas.user_id: user_id
    })
    db.commit()

def update_kassa_minus(id,money,db,user_id):
    old_balance = db.query(Kassas).filter(Kassas.id == id).first()
    new_balance = old_balance.balance - money
    db.query(Kassas).filter(Kassas.id == id).update({
        Kassas.balance: new_balance,
        Kassas.user_id: user_id
    })
    db.commit()
