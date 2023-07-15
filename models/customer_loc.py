from sqlalchemy.orm import relationship,backref

from db import Base
from sqlalchemy import *

from models.users import Users
from models.branches import Branches
from models.customer_locations import Customer_locations
from models.products import Products

class Customer_loc_products(Base):
    __tablename__ = "customer_loc_products"
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(999))
    customer_loc_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    
    user = relationship("Users",foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Customer_loc_products.user_id))
    branch = relationship("Branches",foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Customer_loc_products.branch_id))
    customer_loc = relationship("Customer_locations",foreign_keys=[customer_loc_id],
                          primaryjoin=lambda: and_(Customer_locations.id == Customer_loc_products.customer_loc_id),backref=backref("customer_loc"))
    product = relationship("Products",foreign_keys=[product_id],
                          primaryjoin=lambda: and_(Products.id == Customer_loc_products.product_id))
    