from sqlalchemy import Column, Integer, String, Numeric, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from flask_login import UserMixin


class User(UserMixin, Base):
    """
    Create user's model
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    telegram_name = Column(String(100), unique=True)
    telephone = Column(String(100), unique=True)

    def __str__(self):
        return f'{self.id}-{self.name}'