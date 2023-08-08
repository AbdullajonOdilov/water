from fastapi import HTTPException


def role_admin(user):
    if user.role == "admin":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def role_operator(user):
    if user.role == "operator":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def role_branch_admin(user):
    if user.role == "branch_admin":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')

def role_driver(user):
    if user.role == "driver":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def role_warehouser(user):
    if user.role == "warehouser":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def role_verification(user):
    if user.role not in ["admin", "operator", "driver", "branch_admin", "branch_admin"]:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')