from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

from models.branches import Branches
from models.users import Users


class Suppliers(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    address = Column(String(999))
    map_long = Column(String(999))
    map_lat = Column(String(999))
    branch_id = Column(Integer)
    user_id = Column(Integer)


    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Suppliers.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Suppliers.branch_id))
