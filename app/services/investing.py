# app/services/investing.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud


async def investing(session: AsyncSession):
    """Инвестирование пожертвований в открытые проекты."""
    # Получаем открытые объекты
    charity_projects = await charity_project_crud.get_opened(session)
    donations = await donation_crud.get_opened(session)
    for charity_project in charity_projects:
        for donation in donations:
            if not charity_project.fully_invested:
                # Вычисляем сумму для инвестирования
                invested_amount = min(
                    (charity_project.get_remains_investment()),
                    (donation.get_remains_investment()))
                # Увеличиваем сумму инвестирования
                charity_project.invested_amount += invested_amount
                donation.invested_amount += invested_amount
                # Закрываем объекты при выполнении условий
                charity_project.check_is_fully_invested()
                donation.check_is_fully_invested()

    await session.commit()
