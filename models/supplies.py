from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.products import Products
from models.suppliers import Suppliers
from models.users import Users
from models.branches import Branches
from models.warehouses import Warehouses


class Supplies(Base):
    __tablename__ = "supplies"
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer)
    warehouse_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
    date = Column(DateTime)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    supplier_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Supplies.branch_id))

    supplier = relationship('Suppliers', foreign_keys=[supplier_id],
                        primaryjoin=lambda: and_(Suppliers.id == Supplies.supplier_id))
    
    product = relationship('Products', foreign_keys=[product_id],
                        primaryjoin=lambda: and_(Products.id == Supplies.product_id))
    warehouse = relationship('Warehouses', foreign_keys=[warehouse_id],
                             primaryjoin=lambda: and_(Warehouses.id == Supplies.warehouse_id))
    