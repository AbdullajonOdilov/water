from pydantic import validator
from sqlalchemy.orm import relationship,backref

from db import Base
from sqlalchemy import *

from models.orders import Orders
from models.products import Products

from models.users import Users
from models.warehouse_products import Warehouses_products


class Transfers(Base):
    __tablename__ = "transfers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer)
    warehouse_product_id = Column(Integer)
    quantity = Column(Integer)
    date = Column(Date)
    warehoueser_id = Column(Integer)
    driver_id = Column(Integer)
    status = Column(Boolean)
    
    user = relationship("Users",foreign_keys=[warehoueser_id],
                        primaryjoin=lambda: and_(Users.id == Transfers.warehoueser_id))
    branch = relationship("Users",foreign_keys=[driver_id],
                          primaryjoin=lambda: and_(Users.id == Transfers.driver_id))
    order = relationship('Orders', foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Transfers.order_id))
    w_product = relationship("Warehouses_products", foreign_keys=[warehouse_product_id],
                        primaryjoin=lambda: and_(Warehouses_products.id == Transfers.warehouse_product_id))
    