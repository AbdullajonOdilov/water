from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.users import Users
from models.branches import Branches
from models.customer_locations import Customer_locations


class Contracts(Base):
    __tablename__ = "contracts"
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(999))
    customer_loc_id = Column(Integer)
    quantity = Column(Integer)
    deadline = Column(Date)
    status = Column(String(999))
    user_id = Column(Integer)
    branch_id = Column(Integer)

    
    user = relationship("Users",foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Contracts.user_id))
    branch = relationship("Branches",foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Contracts.branch_id))
    
    customer_location = relationship('Customer_locations', foreign_keys=[customer_loc_id],
                        primaryjoin=lambda: and_(Customer_locations.id == Contracts.customer_loc_id))
    
    