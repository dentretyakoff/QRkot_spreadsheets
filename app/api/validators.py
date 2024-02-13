# app/api/validators.py
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import DEFAULT_AMOUNT
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession) -> None:
    charity_project_id = await (charity_project_crud.
                                get_charity_project_id_by_name(
                                    charity_project_name, session))
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!')


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id,
                                                     session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!')

    return charity_project


async def check_charity_project_before_delete(
        charity_project: CharityProject) -> CharityProject:
    if charity_project.invested_amount > DEFAULT_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!')

    return charity_project


async def check_charity_project_before_edit(
        charity_project: CharityProject,
        obj_in: CharityProjectUpdate) -> CharityProject:
    new_full_amount_less = (
        getattr(obj_in, 'full_amount') or 0) < charity_project.invested_amount
    if new_full_amount_less:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемуя сумма должна быть не меньше уже внесённой!')
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!')

    return charity_project
