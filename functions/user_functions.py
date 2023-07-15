from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.hasher_tekshiradi import hasher
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import get_with_branch, save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.users import Users


def all_users(search, page, limit, status, db,branch_id,role):
    users = db.query(Users).join(Users.phones).options(joinedload(Users.phones))
    if branch_id > 0:
        users = get_with_branch(db,Users,branch_id)
    if role != None:
        users = users.filter(Users.role == role)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted))
    if status:
        users = users.filter(Users.status == "True")
    elif status is None:
        users = users
    else:
        users = users.filter(Users.status == "False")
    users = users.order_by(Users.name.asc())
    return pagination(users, page, limit)


def create_user_r(form, db, thisuser):
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username error")
    if form.role != "admin" and form.role != "operator" and form.role != "warehouser"and form.role != "driver":
        raise HTTPException(status_code=400, detail="Role error!")
    password_hash = hasher(form.password)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=form.password,
        password_hash=password_hash,
        role=form.role,
        branch_id = thisuser.branch_id,
        status="True",
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
            create_phone(name,comment, number, new_user_db.id, thisuser.id, db, 'user',thisuser.branch_id)






def update_user_r(form, db, thisuser):
    if get_in_db(db, Users, form.id) is None or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="User or Phone not found!")

    if form.role != "admin" and form.role != "operator" and form.role != "warehouser"and form.role != "driver":
        raise HTTPException(status_code=400, detail="Role error!")

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



