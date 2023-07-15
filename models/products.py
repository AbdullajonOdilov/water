from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.users import Users
from models.branches import Branches
from models.categories import Categories

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    price = Column(Integer)
    category_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Products.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Products.branch_id))
    category = relationship('Categories', foreign_keys=[category_id],
                             primaryjoin=lambda: and_(Categories.id == Products.category_id))
