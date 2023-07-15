from fastapi import HTTPException
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.categories import Categories

def all_categories(search, page, limit, db,branch_id):
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.filter(Categories.name.like(search_formatted))
    if branch_id > 0:
        categories = db.query(Categories).filter(Categories.branch_id == branch_id)
    else:
        categories = db.query(Categories)
    categories = categories.order_by(Categories.name.asc())
    return pagination(categories, page, limit)


def create_category_y(form, db,current_user):
    if db.query(Categories).filter(Categories.name == form.name).first():
            raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
    else:
        new_category_db = Categories(
            name=form.name,
            comment=form.comment,
            branch_id=current_user.branch_id,
            user_id=current_user.id
        )
        save_in_db(db, new_category_db)


def update_category_y(form, db,thisuser):
    if get_in_db(db, Categories, form.id):
        db.query(Categories).filter(Categories.id == form.id).update({
            Categories.id: form.id,
            Categories.name: form.name,
            Categories.comment: form.comment,
            Categories.branch_id: thisuser.branch_id,
            Categories.user_id: thisuser.id
        })
        db.commit()
