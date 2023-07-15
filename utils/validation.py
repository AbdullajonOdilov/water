from fastapi import HTTPException
from models.branches import Branches
from payments

def Big_checker(db,Model,parametr1,parametr2):
    print(parametr1)
    print("XAXAXAXAXAXAX")
    print(parametr2)
    if Model == Branches:
        if db.query(Branches).filter(parametr1 == parametr2).first():
                raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
        else:
            return True
        
