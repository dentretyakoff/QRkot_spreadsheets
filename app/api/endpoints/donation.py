# app/api/donation.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDBFull, DonationDBShort
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    """Любой пользователь может оставить пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing(session)
    await session.refresh(new_donation)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    """Для суперюзеров. Может получить все пожертвования со всеми полями."""
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationDBShort])
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    """Для пользователей. Может получить свои пожертвования
    с ограниченным набором полей.
    """
    return await donation_crud.get_donations_by_user(session, user)
