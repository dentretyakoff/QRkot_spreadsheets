# app/crud/charity_project.py
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name))
        return db_charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> Optional[list[str]]:
        charity_projects = await session.execute(
            select([
                CharityProject.name,
                (func.strftime('%s', CharityProject.close_date)
                 - func.strftime('%s', CharityProject.create_date)
                 ).label('duration_seconds'),
                CharityProject.description
                ]).where(
                CharityProject.fully_invested).order_by('duration_seconds'))

        return charity_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
