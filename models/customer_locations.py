from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.users import Users
from models.branches import Branches
from models.customers import Customers


class Customer_locations(Base):
    __tablename__ = "customer_locations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    map_long = Column(String(999))
    map_lat = Column(String(999))
    address = Column(String(999))
    orienter = Column(String(999))
    customer_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                                primaryjoin=lambda: and_(Users.id == Customer_locations.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Customer_locations.branch_id))
    
    customer = relationship('Customers', foreign_keys=[customer_id],
                            primaryjoin=lambda: and_(Customers.id == Customer_locations.customer_id),
                            backref=backref("customer_loc"))
    
