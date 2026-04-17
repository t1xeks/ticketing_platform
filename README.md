# HelpDesk Ticketing System

Система Help Desk для учета заявок, созданная на Flask. Приложение позволяет сотрудникам отправлять заявки о проблемах, а службе поддержки - обрабатывать и закрывать их.

## Возможности

- Регистрация и авторизация пользователей (сотрудник, поддержка)
- Создание заявок
- Отслеживание статуса заявок
- Обновление заявок
- REST API для заявок (`/api/issues`)
- Swagger-документация API (`/api/docs/`)
- Клиентская страница с JavaScript-логикой (`/client`)
- Flash-уведомления
- Предсозданный аккаунт администратора

## Архитектура проекта

Проект разделен на слои:
- `ticketing_app/models` — модели БД
- `ticketing_app/services` — бизнес-логика
- `ticketing_app/web` — HTML-контроллеры
- `ticketing_app/api` — JSON API
- `ticketing_app/exceptions.py` — централизованная обработка ошибок

Подробное объяснение для курсовой: `COURSEWORK_EXPLANATION_RU.md`.

## Используемые технологии

- **Flask** - веб-фреймворк Python для создания приложения
- **SQLAlchemy** - ORM и инструменты работы с SQL
- **PostgreSQL** - база данных для хранения пользователей и заявок
- **Flask-WTF** - работа с формами
- **Werkzeug** - хеширование паролей
- **Flask-Login** - управление сессиями пользователей

## Запуск проекта

1. Склонируйте репозиторий.

2. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/macOS
# source env/bin/activate
pip install -r requirements.txt
```

3. Настройте PostgreSQL и укажите параметры подключения в `app.py`.

```sql
CREATE DATABASE ticketing_system;
CREATE USER ticketing_user WITH PASSWORD 'qwerty123';
GRANT ALL PRIVILEGES ON DATABASE ticketing_system TO ticketing_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ticketing_user;
```

4. Запуск без Docker:

В `app.py` используйте:

```python
app.run()
```

Затем запустите:

```bash
python app.py
```

5. Запуск с Docker / Docker Compose:

В `app.py` используйте:

```python
app.run(host='0.0.0.0', port=5000)
```

Затем:

```bash
docker-compose up
```

## Скриншоты приложения

![Login Screen](/pictures/1_login.png)
![Register Screen](/pictures/2_register.png)
![Account Created](/pictures/3_account_created.png)
![Home Page](/pictures/4_home.png)
![Update Account](/pictures/5_update_account.png)
![About Page](/pictures/6_about.png)
![Empty Issues - Employee](/pictures/7_my_issues_empty.png)
![New Issue](/pictures/8_new_issue.png)
![Issue Details](/pictures/9_issue_details.png)
![Issues - Employee](/pictures/10_my_issues.png)
![Issues - Support](/pictures/11_all_issues_admin.png)
![Update Issue - Support](/pictures/12_admin_update_issue.png)
![Updated Issues - Support](/pictures/13_updated_issues.png)
