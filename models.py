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

    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    first_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(50))
    password = Column(String(100))
    telegram_id = Column(String(100), unique=True)
    telegram_username = Column(String(100), unique=True)


    def __str__(self):
        return f'{self.id}-{self.name}'