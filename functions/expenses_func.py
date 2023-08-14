from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.kassa_func import update_kassa_minus
from models.kassa import Kassas
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.expenses import Expenses
from datetime import datetime


def all_expenses(page, limit, db, branch_id):
    expenses_query = db.query(Expenses).options(joinedload(Expenses.this_user),
                                                joinedload(Expenses.kassa),
                                                joinedload(Expenses.this_warehouse))

    if branch_id > 0:
        expenses_query = expenses_query.filter(Expenses.branch_id == branch_id)

    expenses_query = expenses_query.order_by(Expenses.id.desc())
    return pagination(expenses_query, page, limit)


def one_expense(db, ident):
    the_item = db.query(Expenses).filter(Expenses.id == ident).options(joinedload(Expenses.this_user),
                                                joinedload(Expenses.kassa),
                                                joinedload(Expenses.this_warehouse)).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item


def create_expenses_y(form, db, this_user):
    kassa = the_one(form.kassa_id, Kassas, db)
    if form.source not in ['user', 'warehouses']:
        raise HTTPException(status_code=400, detail="source error")
    if form.money <= kassa.balance:
        new_expenses_db = Expenses(
            money=form.money,
            date=datetime.today(),
            user_id=this_user.id,
            branch_id=this_user.branch_id,
            source=form.source,
            source_id=form.source_id,
            kassa_id=form.kassa_id,
            comment=form.commet,
        )
        save_in_db(db, new_expenses_db)
        update_kassa_minus(form.kassa_id, form.money, db, this_user.id)
    else:
        raise HTTPException(status_code=400,detail="Kassada buncha pul mavjud emas!!!")


def update_expenses_y(form, db, this_user):
    if the_one(form.id, Expenses, db):
        old_expenses = the_one(form.id, Expenses, db)
        new_expense_money = old_expenses.money + form.money
        kassa = the_one(old_expenses.kassa_id, Kassas, db)
        if form.source not in ['user', 'warehouses']:
            raise HTTPException(status_code=400, detail="source error")
        if form.money <= kassa.balance:
            db.query(Expenses).filter(Expenses.id == form.id).update({
                Expenses.id: form.id,
                Expenses.money: new_expense_money,
                Expenses.comment: form.comment,
                Expenses.user_id: this_user.id
            })
            db.commit()
            update_kassa_minus(old_expenses.kassa_id, form.money, db, this_user.id)
        else:
            raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud bas")

