from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from db import Base


def get_in_db(
        db: Session,
        model,
        id: int
):
    data = db.query(model).get(id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"bunday foydalanuvchi yoq, notogri parametr kiritdingiz"
        )
    return data

def get_with_branch(
        db: Session,
        model,
        branch_id: int
):
    data = db.query(model).join(model.phones).options(joinedload(model.phones))
    data = data.filter(model.branch_id==branch_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"bunday foydalanuvchi yoq, notogri parametr kiritdingiz yoq"
        )
    return data


def save_in_db(
        db: Session,
        data: Base
):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def yangiledi(
        db: Session,
        data: Base
):
    db.commit()
    db.refresh(data)
    return data
