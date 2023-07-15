from datetime import timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from requests import Session
from functions.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db import SessionLocal
from db import database
from models.users import Users
from functions.hasher_tekshiradi import tekshiradi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def login(db: Session = Depends(database), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).filter(Users.username ==  form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with this: {form_data.username} not found")
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password_hash)
    else:
        is_validate_password = False

    if not is_validate_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parolda xatolik",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # db.query(Users).filter(Users.id == user.id).update({
    #     Users.token: access_token
    # })
    # db.commit()
    return {'id': user.id, "access_token": access_token, "token_type": "bearer", "role": user.role}