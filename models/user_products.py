from sqlalchemy.orm import relationship,backref

from db import Base
from sqlalchemy import *
from models.products import Products

from models.users import Users
from models.branches import Branches


class User_products(Base):
    __tablename__ = "user_products"
    id = Column(Integer,autoincrement=True,primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    
    user = relationship("Users",foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == User_products.user_id))
    branch = relationship("Branches",foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == User_products.branch_id))
    this_product = relationship("Products",foreign_keys=[product_id],
                        primaryjoin=lambda: and_(Products.id == User_products.product_id))
    