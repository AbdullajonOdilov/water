from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.hasher_checker import hasher
from functions.phones_func import create_phone, update_phone
from models.branches import Branches
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.users import Users


def all_users(search, page, limit, status, branch_id, db, thisuser):
    if thisuser.branch_id:
        users = db.query(Users).filter(Users.branch_id == thisuser.branch_id).options(joinedload(Users.phones),
                                                                                      joinedload(Users.branch))
    else:
        users = db.query(Users).options(joinedload(Users.phones),
                                        joinedload(Users.branch))
    if branch_id:
        users = users.filter(Users.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted))
    if status:
        users = users.filter(Users.status==True)
    if status==False:
        users = users.filter(Users.status==False)
    else:
        users = users
    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)

def one_user(db, user, ident):
    the_user = db.query(Users).filter(Users.id == ident).options(joinedload(Users.phones),
                                                                 joinedload(Users.branch)).first()
    if the_user is None:
        raise HTTPException(status_code=404)
    return the_user


def create_user_r(form, db, thisuser): #
    the_one(form.branch_id, Branches, db)
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username error")
    if form.role not in ["admin", "branch_admin", "operator", "warehouser", "driver"]:
        raise HTTPException(status_code=400, detail="Role error!")
    if thisuser.role not in ['admin', 'branch_admin']:
        raise HTTPException(status_code=400, detail='Sizga ruxsat berilmagan')

    password_hash = hasher(form.password)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=form.password,
        password_hash=password_hash,
        role=form.role,
        branch_id=form.branch_id,
        status=form.status,
        balance=0.00, #default
        balance_oylik=form.balance_oylik
    )
    save_in_db(db, new_user_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
            raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
        else:
            name = i.name
            number = i.number
            create_phone(name, comment, number, new_user_db.id, new_user_db.id, db, 'user', new_user_db.branch_id)


def update_user_r(form, db, thisuser):
    # the_one(form.branch_id, Branches, db)
    user = the_one(form.id, Users, db)
    if db.query(Users).filter(Users.username == form.username).first() and user.username != form.username:
        raise HTTPException(status_code=400, detail="Username error")
    if form.role not in ["admin", "branch_admin", "operator", "warehouser", "driver"]:
        raise HTTPException(status_code=400, detail="Role error!")
    if thisuser.role not in ['admin', 'branch_admin']:
        raise HTTPException(status_code=400, detail='Sizga ruxsat berilmagan')
    password_hash = hasher(form.password)
    db.query(Users).filter(Users.id == form.id).update({
        Users.id: form.id,
        Users.name: form.name,
        Users.username: form.username,
        Users.password: form.password,
        Users.password_hash: password_hash,
        Users.role: form.role,
        Users.branch_id: thisuser.branch_id,
        Users.status: form.status,
        Users.balance_oylik: form.balance_oylik
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'user',branch_id = thisuser.branch_id)
