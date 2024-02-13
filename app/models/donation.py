# app/models/donation.py
from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract_model import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return (f'{self.id}. {self.full_amount} - {self.invested_amount}; '
                f'{self.create_date} - {self.close_date}')
