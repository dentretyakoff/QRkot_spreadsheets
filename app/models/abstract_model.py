# app/models/abstract_model.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.config import DEFAULT_AMOUNT
from app.core.db import Base


class AbstractModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer,
                             default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    def check_is_fully_invested(self):
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            self.close_date = datetime.utcnow()

    def get_remains_investment(self):
        return self.full_amount - self.invested_amount
