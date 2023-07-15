from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

engine=create_engine('mysql+pymysql://root@localhost:3306/suv')
SessionLocal=sessionmaker(bind=engine)


Base=declarative_base()


def database():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()