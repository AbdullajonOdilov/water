from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.users import Users
from models.branches import Branches
from models.customer_locations import Customer_locations

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    number = Column(Integer,autoincrement=True)
    operator_id = Column(Integer)
    status = Column(String(999))
    driver_id = Column(Integer)
    warehouser_id = Column(Integer)
    orienter = Column(String(999))
    customer_loc_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Orders.user_id))
    
    this_operator = relationship('Users', foreign_keys=[operator_id],
                        primaryjoin=lambda: and_(Users.id == Orders.operator_id))
    
    this_driver = relationship('Users', foreign_keys=[driver_id],
                        primaryjoin=lambda: and_(Users.id == Orders.driver_id))
    
    this_warehouser = relationship('Users', foreign_keys=[warehouser_id],
                        primaryjoin=lambda: and_(Users.id == Orders.warehouser_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Orders.branch_id))
    
    customer_loc = relationship('Customer_locations', foreign_keys=[customer_loc_id],
                        primaryjoin=lambda: and_(Customer_locations.id == Orders.customer_loc_id))
    
