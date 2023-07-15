from pydantic import validator
from sqlalchemy.orm import relationship,backref

from db import Base
from sqlalchemy import *
from models.products import Products

from models.users import Users
from models.branches import Branches
from datetime import date

class Transfers(Base):
    __tablename__ = "transfers"
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(999))
    product_id = Column(Integer)
    quantity = Column(Integer)
    date = Column(Date)
    warehoueser_id = Column(Integer)
    driver_id = Column(Integer)
    status = Column(String(999))
    
    user = relationship("Users",foreign_keys=[warehoueser_id],
                        primaryjoin=lambda: and_(Users.id == Transfers.warehoueser_id))
    branch = relationship("Users",foreign_keys=[driver_id],
                          primaryjoin=lambda: and_(Users.id == Transfers.driver_id))
    this_product = relationship("Products",foreign_keys=[product_id],
                        primaryjoin=lambda: and_(Products.id == Transfers.product_id))
    