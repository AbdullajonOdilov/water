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
    if user.role == "admin":
        return True
    elif user.role == "operator":
        return True
    elif user.role == "driver":
        return True
    elif user.role == "warehouser":
        return True
    else:
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')