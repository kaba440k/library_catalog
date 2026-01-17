# Library Catalog API

REST API для управления библиотечным каталогом, реализованный на **FastAPI** + **PostgreSQL** + **SQLAlchemy 2.0 (async)**.

# Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone <ваш-репозиторий>
   cd library_catalog
   ```
2. **Установите зависимости:**
    ```bash
    poetry install
    ```
3. **Скопируйте и настройте .env:**
    ```bash
    cp .env.example .env
    ```
4. **Запустите PostgreSQL:**
    ```bash
    docker-compose up -d postgres
    ```
5. **Примените миграции:**
    ```bash
    poetry run alembic upgrade head
    ```

6. **Запустите сервер:**
    ```bash
    poetry run uvicorn src.library_catalog.main:app --reload
    ```

# Основные возможности

- Полный CRUD для книг
- Поиск и фильтрация по названию, автору, жанру, году, доступности
- Пагинация результатов
- Автоматическое обогащение данных из Open Library (обложка, темы, издатель и др.)
- Валидация бизнес-правил (год не в будущем, страницы > 0 и т.д.)
- Доменные исключения и понятные HTTP-ответы
- Health-check эндпоинт
- Полная документация в Swagger и ReDoc
- Поддержка CORS
- Миграции базы через Alembic

# Основные эндпоинты

| Метод | Путь | Описание | Тело / Параметры | Ответ |
|-------|------|----------|------------------|--------|
| POST | `/api/v1/books` | Создать книгу | BookCreate (JSON) | ShowBook (201) |
| GET | `/api/v1/books` | Поиск книг с фильтрами и пагинацией | `title, author, genre, year, available, page, page_size` | PaginatedResponse[ShowBook] |
| GET | `/api/v1/books/{book_id}` | Получить книгу по ID | `book_id (UUID)` | ShowBook |
| PATCH | `/api/v1/books/{book_id}` | Частично обновить книгу | BookUpdate (JSON) | ShowBook |
| DELETE | `/api/v1/books/{book_id}` | Удалить книгу | `book_id (UUID)` | 204 No Content |
| GET | `/api/v1/health` | Проверка состояния сервиса | — | `{"status": "healthy"}` |

# Технологии

| Компонент     | Технология | Версия           | Зачем                                                                        |
|---------------|------------|------------------|------------------------------------------------------------------------------|
| Web Framework | FastAPI    | 0.109+           | Быстрый async framework с автодокументацией                                  |
| ASGI Server   | Uvicorn    | 0.27+            | Запуск async приложения                                                      |
| Database      | PostgreSQL | 16+              | Production-ready СУБД                                                        |
| ORM           | SQLAlchemy | 2.0+             | Async работа с БД                                                            |
| Migrations    | Alembic    | 1.13+            | Версионирование схемы БД                                                     |
| Validation    | Pydantic   | 2.5+             | Валидация через типы                                                         |
| HTTP Client   | httpx      | 0.26+            | Async HTTP запросы                                                           |
| Зависимости   | Poetry     | Последняя версия | Управление зависимости и виртуальным окружением на работе и больших проектах |

# Принципы многослойной архитектуры

Приложение состоит из **четырех независимых слоев**:

```
┌──────────────────────────────────────────────────────┐
│              1. API LAYER (api/)                     │
│  HTTP endpoints, валидация запросов/ответов          │
│                                                      │
└────────────────────┬─────────────────────────────────┘
                     │ вызывает
                     ▼
┌──────────────────────────────────────────────────────┐
│            2. DOMAIN LAYER (domain/)                 │
│  Бизнес-логика, правила, координация                 │
│                                                      │
└──────────────┬───────────────┬───────────────────────┘
               │               │
               │ использует    │ использует
               ▼               ▼
┌──────────────────────┐  ┌──────────────────────┐
│  3. DATA LAYER       │  │  4. EXTERNAL LAYER   │
│  (data/)             │  │  (external/)         │
│  Работа с БД         │  │  Внешние API         │
│  CRUD, запросы       │  │  HTTP клиенты        │
└──────────────────────┘  └──────────────────────┘
```


# Структура проекта
## Полная структура файлов 

```
library_catalog/
│
├── README.md                         # ← Описание проекта
├── pyproject.toml                    # ← Зависимости Poetry
├── .env.example                      # ← Пример конфигурации
├── .gitignore                        # ← Игнор добавления в GIT
├── docker-compose.yml                # ← PostgreSQL в Docker
├── alembic.ini                       # ← Конфиг Alembic
│
├── src/
│   └── library_catalog/
│       ├── __init__.py
│       ├── main.py                   # ← Точка входа
│       │
│       ├── api/                      # API LAYER
│       │   ├── __init__.py
│       │   ├── dependencies.py       # ← DI контейнер
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── routers/
│       │       │   ├── __init__.py
│       │       │   ├── books.py      # ← CRUD эндпоинты
│       │       │   └── health.py     # ← health check
│       │       └── schemas/
│       │           ├── __init__.py
│       │           ├── book.py       # ← Pydantic схемы
│       │           └── common.py     # ← Пагинация
│       │
│       ├── core/                     # CORE
│       │   ├── __init__.py
│       │   ├── config.py             # ← Settings
│       │   ├── database.py           # ← Async engine
│       │   ├── logging_config.py     # ← Логирование
│       │   └── exceptions.py         # ← Базовые исключения
│       │
│       ├── data/                     # DATA LAYER
│       │   ├── __init__.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── book.py           # ← SQLAlchemy модель
│       │   └── repositories/
│       │       ├── __init__.py
│       │       ├── base_repository.py # ← Базовый класс
│       │       └── book_repository.py # ← CRUD для книг
│       │
│       ├── domain/                   # DOMAIN LAYER
│       │   ├── __init__.py
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   └── book_service.py   # ← Бизнес-логика
│       │   ├── exceptions.py         # ← Доменные ошибки
│       │   └── mappers/
│       │       ├── __init__.py
│       │       └── book_mapper.py    # Создать: Entity ↔ DTO
│       │
│       ├── external/                 # EXTERNAL LAYER
│       │   ├── __init__.py
│       │   ├── base/
│       │   │   ├── __init__.py
│       │   │   └── base_client.py    # HTTP базовый клиент
│       │   └── openlibrary/
│       │       ├── __init__.py
│       │       ├── client.py         # Open Library API
│       │       └── schemas.py        # схемы ответов
│       │   
│       │
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
├── alembic/
│   ├── versions/                     # ← Миграции создаются автоматически
│   ├── env.py                        # ← Настройки для async
│   └── script.py.mako
│
└── tests/
    ├── __init__.py                
    ├── unit/   
    └── integration/
        └── OpenLibraryTest.py        # ← Тест подключения к OpenLibrary
```
# Обогащение данных

### При создании книги (если передан ISBN или title + author) автоматически запрашиваются дополнительные данные из **Open Library**:

- URL обложки
- Список тем/жанров
- Издатель
- Язык
- Средний рейтинг

Данные сохраняются в поле **extra (JSONB)**.
Если **Open Library** недоступен — книга создаётся без обогащения, в лог пишется **warning**.