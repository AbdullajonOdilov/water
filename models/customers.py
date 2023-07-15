from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.users import Users
from models.branches import Branches

class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    type = Column(String(999))
    comment = Column(String(999))
    user_id = Column(Integer)
    branch_id = Column(Integer)
    balance = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Customers.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Customers.branch_id))
