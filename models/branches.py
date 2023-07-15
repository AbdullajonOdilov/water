from db import Base
from sqlalchemy import *



class Branches(Base):
    __tablename__ = "branches"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    adress = Column(String(999))
    map_long = Column(String(999))
    map_lat = Column(String(999))
    status = Column(String(999))