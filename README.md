# Задание 1. Phone Address API

Это RESTful API сервис для управления данными о номерах телефонов и их связанных адресах с использованием FastAPI, Redis и асинхронных функций. API позволяет записывать, обновлять и получать данные об адресах по номерам телефонов.

## Стек технологий

- Python 3.10+
- FastAPI
- Redis (асинхронный клиент Redis)
- Pydantic
- Docker & Docker Compose
- pytest для тестирования

## Установка и запуск

### Клонирование репозитория

```bash
git clone git@github.com:poligrafo/phone-address-api.git
cd phone-address-api
```

## Настройка переменных окружения

Проект использует файл `.env` для хранения конфигураций. В репозитории уже есть пример файла с переменными окружения:

```bash
cp .envexample .env
```
Откройте файл .env и при необходимости настройте переменные окружения, такие как хост и порт Redis:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DEBUG=True
```

## Запуск с использованием Docker

Соберите и запустите контейнеры:

```bash
docker-compose up --build

