from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

from models.branches import Branches


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    username = Column(String(999))
    password = Column(String(999))
    password_hash = Column(String(999))
    status = Column(Boolean)
    role = Column(String(999))
    branch_id = Column(Integer)
    balance = Column(Numeric)
    balance_oylik = Column(Integer)
    token = Column(String(999), default='token')

    branch = relationship("Branches", foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Users.branch_id))