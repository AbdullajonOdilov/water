from fastapi import HTTPException

from models.branches import Branches
from models.users import Users
from utils.db_operations import save_in_db, get_in_db, the_one
from utils.paginatsiya import pagination
from models.categories import Categories


def all_categories(search, page, limit, db, branch_id):
    categories = db.query(Categories)
    if branch_id > 0:
        categories = db.query(Categories).filter(Categories.branch_id == branch_id)
    else:
        categories = db.query(Categories)
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.filter(Categories.name.like(search_formatted))
    categories = categories.order_by(Categories.id.desc())
    return pagination(categories, page, limit)


def create_category_y(form, db, current_user):
    # user = db.query(Users).filter(Users.id == current_user.id).first()
    new_category_db = Categories(
        name=form.name,
        comment=form.comment,
        branch_id=current_user.branch_id,
        user_id=current_user.id
    )
    save_in_db(db, new_category_db)


def update_category_y(form, db, thisuser):
    the_one(form.id, Categories, db)
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.branch_id: thisuser.branch_id,
        Categories.user_id: thisuser.id
    })
    db.commit()
