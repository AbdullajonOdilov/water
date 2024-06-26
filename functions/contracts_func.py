from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.warehouse_products import Warehouses_products
from utils.db_operations import save_in_db, get_in_db, the_one
from utils.paginatsiya import pagination
from models.contracts import Contracts


def all_contracts_r(page, limit, db, branch_id):
    contracts = db.query(Contracts).options(joinedload(Contracts.warehouse_product),
                                            joinedload(Contracts.user))
    if branch_id > 0:
        contracts = contracts.filter(Contracts.branch_id == branch_id)
    contracts = contracts.order_by(Contracts.id.desc())
    return pagination(contracts, page, limit)


def one_contract(ident, db):
    the_item = db.query(Contracts).filter(Contracts.id == ident).options(
        joinedload(Contracts.warehouse_product), joinedload(Contracts.user)
    ).first()
    if the_item is None:
        raise HTTPException(status_code=404)
    return the_item


def create_contract_y(form, db, this_user):
    the_one(form.warehouse_product_id, Warehouses_products, db)
    new_contract_db = Contracts(
        warehouse_product_id=form.warehouse_product_id,
        quantity=form.quantity,
        deadline=form.deadline,
        status=True,
        user_id=this_user.id,
        branch_id=this_user.branch_id
    )
    save_in_db(db, new_contract_db)


def update_contract_y(form, db, this_user):
    the_one(form.warehouse_product_id, Warehouses_products, db)
    db.query(Contracts).filter(Contracts.id == form.id).update({
        Contracts.quantity: form.quantity,
        Contracts.deadline: form.deadline,
        Contracts.status: form.status,
        Contracts.user_id: this_user.id
    })
    db.commit()

