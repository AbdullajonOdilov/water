from models.warehouse_products import Warehouses_products
from utils.db_operations import save_in_db, get_in_db, the_one
from utils.paginatsiya import pagination
from models.contracts import Contracts


def all_contracts_r(search, page, limit, db, branch_id):
    contracts = db.query(Contracts)
    if branch_id > 0:
        contracts = db.query(Contracts).filter(Contracts.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        contracts = contracts.filter(Contracts.name.like(search_formatted))
    else:
        search_filter = Contracts.id > 0
    contracts = db.query(Contracts).filter(search_filter).order_by(Contracts.name.asc())
    return pagination(contracts, page, limit)


def create_contract_y(form, db, this_user):
    the_one(form.warehouse_product_id, Warehouses_products, db)
    new_contract_db = Contracts(
        warehouses_product_id=form.warehouses_product_id,
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

