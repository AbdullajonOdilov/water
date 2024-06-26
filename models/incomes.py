from sqlalchemy.orm import relationship, backref
from db import Base
from sqlalchemy import *
from models.branches import Branches
from models.kassa import Kassas
from models.orders import Orders

from models.users import Users


class Incomes(Base):
    __tablename__ = "incomes"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    date = Column(Date)
    comment = Column(String(999))
    kassa_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)
    source = Column(String(999))
    source_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Incomes.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Incomes.branch_id))
    this_user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Incomes.source_id, Incomes.source == "user"), backref=backref("income"))
    this_order = relationship('Orders', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Orders.id == Incomes.source_id, Incomes.source == "order"), backref=backref("income"))

    kassa = relationship('Kassas', foreign_keys=[kassa_id],
                         primaryjoin=lambda: and_(Kassas.id == Incomes.kassa_id), backref=backref("income"))

