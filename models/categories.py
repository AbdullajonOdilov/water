from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.users import Users
from models.branches import Branches


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Categories.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Categories.branch_id))
