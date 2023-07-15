from utils.db_operations import save_in_db
from utils.paginatsiya import pagination
from models.phones import Phones


def all_phones(search, page, limit, db,branch_id):
    phones = db.query(Phones)
    if branch_id > 0:
        phones = phones.filter(Phones.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = phones.filter(Phones.number.like(search_formatted))
    else:
        search_filter = Phones.id > 0
    phones = phones.filter(search_filter).order_by(Phones.number.asc())
    return pagination(phones, page, limit)


def create_phone(name,comment, number, source_id, user_id, db, source,branch_id):
        new_phone_db = Phones(
            name=name,
            number=number,
            comment=comment,
            source=source,
            source_id=source_id,
            user_id=user_id,
            branch_id=branch_id
        )
        save_in_db(db, new_phone_db)




def update_phone(phone_id, comment, number, source_id, user_id, db, source,branch_id):
    db.query(Phones).filter(Phones.id == phone_id).update({
        Phones.number: number,
        Phones.comment: comment,
        Phones.source: source,
        Phones.source_id: source_id,
        Phones.user_id: user_id,
        Phones.branch_id: branch_id
    })
    db.commit()

