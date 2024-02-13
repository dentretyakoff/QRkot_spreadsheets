# app/api/charity_project.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_before_edit,
                                check_charity_project_exists,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Только суперюзер может создавать проекты."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session)
    await investing(session)
    await session.refresh(new_charity_project)

    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    """Все пользователи могут просматривать список проектов."""
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def delete_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """Для суперюзеров. Можно удалить проекты только без пожертвований."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    charity_project = await check_charity_project_before_delete(
        charity_project)

    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)):
    """Для суперюзеров. Модифицировать закрытые проекты запрещено."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await check_charity_project_before_edit(
        charity_project, obj_in)

    return await charity_project_crud.update(db_obj=charity_project,
                                             obj_in=obj_in,
                                             session=session)
