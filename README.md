# Hotel Booking API

Асинхронный бэкенд на FastAPI для бронирования номеров: авторизация, каталог отелей и комнат, брони с проверкой доступности, SQLAdmin и простое демо-UI.

## Стек

- **FastAPI** + **Uvicorn**
- **PostgreSQL** через **SQLAlchemy** (async) + **asyncpg**
- Миграции **Alembic**
- **JWT** в HttpOnly-cookies (`python-jose` + `passlib`/`bcrypt`)
- **SQLAdmin** по адресу `/admin`
- Простой фронтенд в `frontend/`
- **Redis** для кэширования данных
- **Docker** для запуска

## Требования

- Python 3.14+
- PostgreSQL
- Redis
- [uv](https://github.com/astral-sh/uv) (рекомендуется)

## Установка

```bash
.env-non-dev # некоторые данные уже есть, необходимо заполнить SECRET_KEY и ALGORITHM
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

Для защищённых эндпоинтов используется cookie `booking_access_token`.

## Структура проекта

```
bookings/   hotels/   rooms/   users/   # доменные модули
service/    # общий BaseService
frontend/   # демо-UI
migrations/ # Alembic
main.py     # точка входа + SQLAdmin
config.py   # настройки из .env
.env-non-dev # для Docker
Dockerfile # докер без сервисов
docker-compose.yml # докер с сервисами
```