from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from models.categories import Categories
from models.products import Products
from models.supplies import Supplies
from models.users import Users
from models.branches import Branches
from models.customers import Customers
from models.warehouse_products import Warehouses
from sqlalchemy import TEXT,Text


class Uploaded(Base):
    __tablename__ = "uploaded"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file = Column(String(999))
    comment = Column(String(999))
    source = Column(String(999))
    source_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Uploaded.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Uploaded.branch_id))

    this_user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Uploaded.source_id, Uploaded.source == "user"), backref=backref("uploaded"))
    
    this_branch = relationship('Branches', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Branches.id == Uploaded.source_id, Uploaded.source == "branch"), backref=backref("uploaded"))
    
    this_customer = relationship('Customers', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Customers.id == Uploaded.source_id, Uploaded.source == "customers"), backref=backref("uploaded"))
    
    this_warehouse = relationship('Warehouses', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Warehouses.id == Uploaded.source_id, Uploaded.source == "warehouses"), backref=backref("uploaded"))

    this_supplier = relationship('Supplies', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Supplies.id == Uploaded.source_id, Uploaded.source == "supplies"), backref=backref("uploaded"))

    product = relationship("Products", foreign_keys=[source_id],
                           primaryjoin=lambda: and_(Products.id == Uploaded.source_id, Uploaded.source == "product"), backref=backref("uploaded"))

    category = relationship("Categories", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Categories.id == Uploaded.source_id, Uploaded.source == "category"), backref=backref("uploaded"))
    

