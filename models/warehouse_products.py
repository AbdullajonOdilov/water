from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.users import Users
from models.branches import Branches
from models.products import Products
from models.warehouses import Warehouses

class Warehouses_products(Base):
    __tablename__ = "warehouses_products"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
    branch_id = Column(Integer)
    warehouse_id = Column(Integer)

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Warehouses_products.branch_id))
    product = relationship('Products', foreign_keys=[product_id],
                             primaryjoin=lambda: and_(Products.id == Warehouses_products.product_id))
    warehouse = relationship('Warehouses', foreign_keys=[warehouse_id],
    primaryjoin=lambda: and_(Warehouses.id == Warehouses_products.warehouse_id))
