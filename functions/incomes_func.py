from datetime import datetime, timedelta
from http.client import HTTPException
from functions.kassa_func import update_kassa_r
from models.incomes import Incomes
from models.kassa import Kassas
from models.orders import Orders
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_income_r(search, page, limit, db,branch_id):
    income = db.query(Incomes)
    if branch_id > 0:
        income = income.filter(Incomes.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Incomes.name.like(search_formatted))
    else:
        search_filter = Incomes.id > 0
    income = income.filter(search_filter).order_by(Incomes.name.asc())
    return pagination(income, page, limit)


def create_income_r(form,db,thisuser):
    kassa = get_in_db(db,Kassas,form.kassa_id)
    if kassa:
        new_income = Incomes(
            name=form.name,
            money=form.money,
            date=datetime.today(),
            comment=form.comment,
            kassa_id=form.kassa_id,
            user_id=thisuser.id,
            branch_id=thisuser.branch_id,
            type=form.type,
            source=form.source,
            source_id=form.source_id
        )
        save_in_db(db, new_income)

        if form.source == "order":
            order = db.query(Orders).filter(Orders.id == form.source_id).first()
            if order:
                order.status == "2"
                save_in_db(db,order)
                update_kassa_r(form.kassa_id,form.money,db,thisuser.id)
        update_kassa_r(form.kassa_id,form.money,db,thisuser.id)

def update_income_e(form, db, thisuser):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Incomes, form.id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    if get_in_db(db, Orders, form.source_id) and form.source == "order":
        old_money = get_in_db(db, Incomes, form.id).money
        db.query(Incomes).filter(Incomes.id == form.id).update({
            Incomes.id: form.id,
            Incomes.money: form.money,
            Incomes.source: form.source,
            Incomes.source_id: form.source_id,
            Incomes.kassa_id: form.kassa_id,
            Incomes.comment: form.comment,
            Incomes.branch_id: thisuser.branch_id,
            Incomes.date: datetime.today(),
            Incomes.name: form.name
        })
        db.commit()
        new_money = get_in_db(db, Incomes, form.id).money
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - old_money + new_money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")

def delete_income_e(id, db):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Incomes, id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Incomes, id)
    db.query(Incomes).filter(Incomes.id == id).delete()
    db.commit()

