from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.transfers import Transfers


def all_transfers(search, page, limit, db):
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Transfers.name.like(search_formatted))
    else :
        search_filter = Transfers.id > 0
    transfers = db.query(Transfers).filter(search_filter).order_by(Transfers.date.asc())
    return pagination(transfers, page, limit)


def create_transfers_y(form, db,this_user):
    new_transfers_db = Transfers(
        name=form.name,
        quantity=form.quantity,
        date=form.date,
        warehoueser_id=form.warehoueser_id,
        driver_id=form.driver_id,
        status=form.status

    )
    save_in_db(db, new_transfers_db)


def update_transfers_y(form,db,this_user):
    if get_in_db(db, Transfers, form.id):
        db.query(Transfers).filter(Transfers.id == form.id).update({
            Transfers.id: form.id,
            Transfers.name: form.name,
            Transfers.quantity: form.quantity,
            Transfers.date: form.date,
            Transfers.warehoueser_id: form.warehoueser_id,
            Transfers.driver_id: form.driver_id,
            Transfers.status: form.status
        })
        db.commit()

