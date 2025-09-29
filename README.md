# Test async

REST API для справочника **Организаций, Зданий и Видов деятельности**.
Проект реализован на **FastAPI + SQLAlchemy + Alembic + PostgreSQL** и завернут в Docker.

---

## Структура проекта

```
test_async/
│
├── app/                   # Основное приложение
│   ├── core/              # Конфигурации и база
│   │   ├── config.py      # Настройки проекта
│   │   ├── database.py    # Подключение к БД
│   │   └── dependencies.py
│   │
│   ├── models/            # SQLAlchemy-модели
│   ├── schemas/           # Pydantic-схемы
│   ├── services/          # CRUD и бизнес-логика
│   │   ├── crud_activity.py
│   │   ├── crud_building.py
│   │   ├── crud_organization.py
│   │   ├── base.py
│   │   ├── seed.py        # Скрипт наполнения тестовыми данными
│   │   └── validators.py
│   │
│   ├── routers/           # Роутеры API
│   │   ├── endpoints/     # Эндпоинты (Activity, Building, Organization)
│   │   │   ├── activity.py
│   │   │   ├── building.py
│   │   │   └── organization.py
│   │   └── routers.py     # Подключение всех маршрутов
│   │
│   └── main.py            # Точка входа FastAPI-приложения
│
├── migrations/            # Alembic миграции
├── docker-compose.yml     # Docker Compose конфигурация
├── Dockerfile             # Docker образ API
├── alembic.ini            # Настройки Alembic
├── requirements.txt       # Python зависимости
├── .env                   # Переменные окружения
└── README.md              # Документация проекта
```

---

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/slava225678/test_async.git
cd secunda_test_task
```

### 2. Настройка виртуального окружения (локально, без Docker)

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создай файл `.env` в корне проекта со следующим содержимым:

```env
API_KEY="supersecretkey"

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://admin:secret@db:5432/secunda_project
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=secunda_project
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 4. Запуск с Docker

```bash
docker-compose up --build
```

После запуска приложение будет доступно по адресу:
[http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
[http://localhost:8000/redoc](http://localhost:8000/redoc) (Redoc)

### 5. Миграции

Создать новую миграцию:

```bash
alembic revision --autogenerate -m "init"
```

Применить миграции:

```bash
alembic upgrade head
```

### 6. Наполнение БД тестовыми данными

Для заполнения базы тестовыми данными используется скрипт `seed.py`.
Запускается из корневой директории:

```bash
python -m app.services.seed
```

---

## Документация API

Документация доступна после запуска:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Используемый стек

* **Python 3.12**
* **FastAPI** — фреймворк для API
* **SQLAlchemy (async)** — ORM
* **Alembic** — миграции
* **PostgreSQL** — база данных
* **Docker / docker-compose** — контейнеризация

