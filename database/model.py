from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import BigInteger, VARCHAR, ForeignKey, DateTime, Boolean, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import base


class UsersTable(base):
    __tablename__ = 'users'

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id: int = Column(Integer, primary_key=True)
    entry: datetime = Column(DateTime, nullable=False)
    subscription: datetime = Column(DateTime)