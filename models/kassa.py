from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.branches import Branches

from models.users import Users


class Kassas(Base):
    __tablename__ = "kassas"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    balance = Column(Numeric)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Kassas.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Kassas.branch_id))
