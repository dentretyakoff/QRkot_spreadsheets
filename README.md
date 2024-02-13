# QRKot
Приложение для Благотворительного фонда поддержки котиков QRKot. 
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
Приложение может формировать и сохранять на гугл-диск отчет по закрытым проектам.

### Тенологии
```
fastapi==0.78.0
pydantic==1.9.1
sqlalchemy==1.4.36
aiogoogle==4.2.0
```

## Установка и настройка
- Клонируйте репозиторий: `git clone git@github.com:dentretyakoff/cat_charity_fund.git`
- Перейдите в директорию проекта: `cd ваш-репозиторий`
- Создайте и активируйте виртуальное окружение:\
  - Linux - `python3 -m venv venv && source venv/bin/activate`\
  - Windows - `python -m venv venv && venv/Scripts/activate`
- Обновите pip:\
    - Linux - `python3 -m pip install -U pip`
    - Windows - `python -m pip install -U pip`
- Установите зависимости: `pip install -r requirements.txt`
- Создайте и заполните файл `.env`
    ```
        APP_TITLE=Благотворительный фонд поддержки котиков QRKot
        DESCRIPTION=Описание
        DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
        SECRET=Secret_key
        FIRST_SUPERUSER_EMAIL=admin@admin.ru
        FIRST_SUPERUSER_PASSWORD=password
        TYPE=service_account
        PROJECT_ID=test-test-000111
        PRIVATE_KEY_ID=asdasdasd1231288a96251113asdasda12
        PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour_Private_Key\n-----END PRIVATE KEY-----\n"
        CLIENT_EMAIL=your_service_account@test-test-000111.iam.gserviceaccount.com
        CLIENT_ID=18273617823617823123123
        AUTH_URI=https://accounts.google.com/o/oauth2/auth
        TOKEN_URI=https://oauth2.googleapis.com/token
        AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
        CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your_service_account%40test-test-000111.iam.gserviceaccount.com
        EMAIL=your_email@gmail.com
    ```
- Примените миграции `alembic upgrade head`
`*Для получения параметров подключения к Google-API необходимо произвести настройки в Google Cloud Platform и получить JSON-файл с ключом доступа к сервисному аккаунту.` [Подробная инструкция](https://developers.google.com/sheets/api/quickstart/python?hl=en)

## Использование
Из дериктории с проектом выполните команду для запуска сервера разработки:
```
uvicorn app.main:app --reload
```
Документация к API доступна по адресам
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Процесс «инвестирования»
Сразу после создания нового проекта или пожертвования запускается процесс «инвестирования» (увеличение `invested_amount` как в пожертвованиях, так и в проектах, установка значений `fully_invested` и `close_date`, при необходимости). 
Если создан новый проект, а в базе были «свободные» (не распределённые по проектам) суммы пожертвований — они автоматически  инвестируются в новый проект. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования автоматически зачисляются на их счета.
## Отчет по закрытым проектам
Суперпользователь может отправить POST-запрос на `http://127.0.0.1:8000/google/` для формирования списка закрытых проектов на гугл-диске пользователя указанного в параметре `EMAIL` файла `.env`.


### Авторы
[Денис Третьяков](https://github.com/dentretyakoff)
### Лицензия
[MIT License](https://opensource.org/licenses/MIT)
