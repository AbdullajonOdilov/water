from db import Base
from sqlalchemy import *

from models.branches import Branches
from sqlalchemy.orm import relationship, backref


class Warehouses(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    address = Column(String(999))
    map_long = Column(String(999))
    map_lat = Column(String(999))
    branch_id = Column(Integer)

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Warehouses.branch_id))