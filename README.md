# Hotel Booking API

Асинхронный бэкенд на FastAPI для бронирования номеров: авторизация, каталог отелей и комнат, брони с проверкой доступности, SQLAdmin, кэширование, очередь сообщений, Docker, мониторинг и простое демо-UI.

## Стек

- **FastAPI** + **Uvicorn**
- **PostgreSQL** через **SQLAlchemy** (async) + **asyncpg**
- Миграции **Alembic**
- **JWT** в HttpOnly-cookies (`python-jose` + `passlib`/`bcrypt`)
- **SQLAdmin** по адресу `/admin`
- Простой фронтенд в `templates/`
- **Redis** для кэширования данных
- **Docker** для запуска
- **Celery/Flower** для очереди и UI демонстрации
- **Prometheus/Grafana** для мониторнга
- **Pytest** для тестов

## Требования

- Python 3.14+
- PostgreSQL
- Redis
- Docker
- [uv](https://github.com/astral-sh/uv) (рекомендуется)

## Установка

```bash
.env-non-dev
docker compose build
```


Применить миграции:

```bash
docker compose exec booking alembic revision --autogenerate -m "initial"
docker compose exec booking alembic upgrade head
```

## Запуск

```bash
docker compose up
```

## Обзор API

| Метод | Путь | Описание |
|--------|------|-------------|
| `POST` | `/auth/register` | Регистрация |
| `POST` | `/auth/login` | Вход (ставит cookie) |
| `POST` | `/auth/logout` | Выход |
| `GET` | `/auth/me` | Текущий пользователь |
| `GET` | `/hotels`, `/hotels/{id}` | Отели |
| `GET` | `/rooms`, `/rooms/{id}` | Комнаты |
| `GET` | `/bookings` | Мои бронирования |
| `GET` | `/bookings/{id}` | Бронь по id |
| `POST` | `/bookings` | Создать бронь (`room_id`, `date_from`, `date_to`) |
| `POST` | `/images/hotels` | Загрузить изображение для отеля (`name`) |
| `GET` | `/prometheus/get_error` | Получить ошибку |
| `GET` | `/prometheus/time_consumer` | Проверить потребление времени |
| `GET` | `/prometheus/memory_consumer` | Проверить потребление памяти |


Для защищённых эндпоинтов используется cookie `booking_access_token`.

## Структура проекта

```
admin/ # админка
bookings/   hotels/   rooms/   users/   # доменные модули
pages/ # роутер frontend'a
prometheus/ # роутеры для получения ошибок
service/    # общий BaseService
static/   # css, js + загрузка файлов
tasks/ # celery
templates/ # html
tests/ # pytest
migrations/ # Alembic
main.py     # точка входа + SQLAdmin
config.py   # настройки из .env
conftest.py # для работы с pytest
.env-non-dev # для Docker
Dockerfile # докер без сервисов
docker-compose.yml # докер с сервисами
prometheus.yml # для мониторинга
```