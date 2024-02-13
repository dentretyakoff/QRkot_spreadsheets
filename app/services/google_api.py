# app/services/google_api.py
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import (COLUMN_COUNT, FORMAT, LOCALE, ROW_COUNT, SHEET_ID,
                             SHEET_NAME, TABLE_RANGE, settings)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': LOCALE},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': SHEET_ID,
                                   'title': SHEET_NAME,
                                   'gridProperties': {
                                       'rowCount': ROW_COUNT,
                                       'columnCount': COLUMN_COUNT}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    spreadsheetid = response['spreadsheetId']

    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheetid,
                                   json=permissions_body,
                                   fields='id'))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [('Отчёт от', now_date_time),
                    ('Топ проектов по скорости закрытия',),
                    ('Название проекта', 'Время сбора', 'Описание')]
    for project in charity_projects:
        new_row = (str(project['name']),
                   str(timedelta(seconds=project['duration_seconds'])),
                   str(project['description']))
        table_values.append(new_row)
    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(spreadsheetId=spreadsheetid,
                                           range=TABLE_RANGE,
                                           valueInputOption='USER_ENTERED',
                                           json=update_body))
