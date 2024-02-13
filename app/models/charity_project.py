# app/models/charity_project.py
from sqlalchemy import Column, String, Text

from app.core.config import MAX_LEN_NAME_PROJECT

from .abstract_model import AbstractModel


class CharityProject(AbstractModel):
    name = Column(String(MAX_LEN_NAME_PROJECT),
                  unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (f'{self.id}. {self.name} - {self.full_amount}; '
                f'{self.create_date} - {self.close_date}')
