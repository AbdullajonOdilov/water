from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *


class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(999), default='')
    body = Column(String(999), default='')
    user_id = Column(Integer, ForeignKey('users.id'), default=0)

    user = relationship('Users', backref="notifications")
