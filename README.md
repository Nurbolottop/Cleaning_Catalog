
# CatalogKIKI — Backend

Backend часть проекта **CatalogKIKI** (Django) с инфраструктурой для разработки и продакшна через Docker.

В составе:

- Django (папка `app/`)
- Postgres (`db_catalog`)
- Redis (`redis_catalog`)
- Отдельный сервис `telegram_bot` (запускается командой `python manage.py bot`, если используется)

## Быстрый старт (dev)

### 1) Переменные окружения

В корне `Backend/` есть пример: `.envtest`.

Создай `.env`:

```bash
cp .envtest .env
```

Минимум, что нужно проверить в `.env`:

- `SECRET_KEY`
- `DEBUG=True` (только для разработки)
- `ALLOWED_HOSTS` (через запятую)
- `LANGUAGE_CODE`, `TIME_ZONE`
- `PROJECT_NAME` (например `catalogkiki`)

Postgres (для docker-compose):

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST=db_catalog` (важно: должно совпадать с именем сервиса БД в compose)
- `POSTGRES_PORT=5432`

### 2) Запуск dev окружения

```bash
docker compose -f docker/docker-compose.yml up --build
```

Что поднимается:

- Postgres: проброшен наружу как `5433:5432`
- Redis: проброшен наружу как `6389:6379`
- Django dev server: внутри `0.0.0.0:8082`, наружу `127.0.0.1:8084`

Открывай:

- `http://127.0.0.1:8084`

## Полезные команды (внутри контейнера web)

- Миграции: `python manage.py migrate`
- Создать админа: `python manage.py createsuperuser`
- Собрать статику: `python manage.py collectstatic --noinput`

## Запуск telegram bot (опционально)

В dev/prod compose есть сервис `telegram_bot`.

Если бот используется — убедись, что необходимые переменные для бота добавлены в `.env` (токен и т.д., если требуется вашей реализацией).

## Продакшн

```bash
docker compose -f docker/docker-compose.prod.yml up --build -d
```

В прод-конфиге Django запускается через gunicorn и слушает `0.0.0.0:8000` (проброшено наружу как `8000:8000`).

## Структура проекта

- `app/` — Django проект (`core.settings`)
- `docker/` — Dockerfile и docker-compose
- `scripts/entrypoint.sh` — entrypoint контейнера
- `.envtest` — пример переменных окружения

## Типовые проблемы

- Если Postgres не поднимается — проверь `POSTGRES_*` в `.env` и что `POSTGRES_HOST=db_catalog`.
- Если порты заняты — поменяй внешние порты в `docker/docker-compose.yml`.
