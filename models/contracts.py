from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.users import Users
from models.branches import Branches
from models.warehouse_products import Warehouses_products


class Contracts(Base):
    __tablename__ = "contracts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    warehouse_product_id = Column(Integer)
    quantity = Column(Integer)
    deadline = Column(Integer)
    status = Column(Boolean)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Contracts.user_id))
    branch = relationship("Branches", foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Contracts.branch_id))
    warehouse_product = relationship('Warehouses_products', foreign_keys=[warehouse_product_id],
                                     primaryjoin=lambda: and_(Warehouses_products.id == Contracts.warehouse_product_id))
    
    