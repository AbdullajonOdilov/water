from datetime import date
from pydantic import validator
from sqlalchemy.orm import relationship,backref

from db import Base
from sqlalchemy import *

from models.users import Users
from models.branches import Branches
from models.kassa import Kassas
from models.warehouses import Warehouses

class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(999))
    money = Column(Numeric)
    date = Column(Date)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    source = Column(String(999))
    source_id = Column(Integer)
    kassa_id = Column(Integer)
    comment = Column(String(999))
    type = Column(String(999))

    user = relationship("Users",foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Expenses.user_id))
    branch = relationship("Branches",foreign_keys=[branch_id],
                          primaryjoin=lambda: and_(Branches.id == Expenses.branch_id))
    kassa = relationship("Kassas",foreign_keys=[kassa_id],
                          primaryjoin=lambda: and_(Kassas.id == Expenses.kassa_id))
    this_user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Expenses.source_id, Expenses.source == "user"), backref=backref("expenses"))
    
    this_warehouse = relationship('Warehouses', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Warehouses.id == Expenses.source_id, Expenses.source == "warehouses"), backref=backref("warehouses"))
