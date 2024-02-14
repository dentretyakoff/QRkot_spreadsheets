# app/services/google_api.py
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import (COLUMN_COUNT, DRIVE_API_VERSION, FORMAT, LOCALE,
                             ROW_COUNT, SHEET_ID, SHEET_NAME,
                             SHEETS_API_VERSION, TABLE_RANGE, settings)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_API_VERSION)
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

    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', DRIVE_API_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheet_id,
                                   json=permissions_body,
                                   fields='id'))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_API_VERSION)
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
        service.spreadsheets.values.update(spreadsheetId=spreadsheet_id,
                                           range=TABLE_RANGE,
                                           valueInputOption='USER_ENTERED',
                                           json=update_body))
