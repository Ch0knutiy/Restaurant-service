# Restaurant service

---

## Technologies
[<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>](https://docs.python.org/3.11/)
[<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>](https://fastapi.tiangolo.com)
[<img src="https://img.shields.io/badge/sqlalchemy-CC2927?style=for-the-badge"/>](https://www.sqlalchemy.org)
[<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white"/>](https://docs.pytest.org/en/7.4.x/)
[<img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>](https://www.postgresql.org)
[<img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>](https://redis.io)
[<img src="https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white"/>](https://docs.celeryq.dev/en/stable/)
[<img src="https://img.shields.io/badge/rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white"/>](https://www.rabbitmq.com)
[<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>](https://www.docker.com)

---

## Description
учебный проект для практики использования FastAPI.

Реализовано:
- API для CRUD операций с сущностями БД.
- Вывод полного списка меню с вложенными подменю и блюдами.
- Кеширование запросов с помощью Redis.
- Инвалидация кеша в background tasks.
- Интеграционное тестирование эндпоинтов с использованием Pytest + httpx.
- Тестовый сценарий для проверки подсчета количества блюд и подменю.
- Фоновое сохранение текущего состояния меню в виде xlsx файла с использованием Celery + RabbitMQ

---

Бизнес логика: - app/services

Взаимодействие с базой данных: - app/repositories

Модели сущностей базы данных: - app/models

Схемы Pydantic: - app/schemas

Задачи для Celery: -  app/tasks

Роутеры: - app/api

Тесты: tests/

---

## Project setup

Запуск приложения
```sh
docker-compose up
```
После запуска на localhost:8000 будет доступно приложение FastAPI

Документация: localhost:8000/docs#/

---

## Testing

Запуск приложения с тестами (запускаяется на тех же портах, что и основное приложение)
```sh
docker-compose -f docker-compose-test.yml up
```

---

## To do
- [X] Сохранение в xlsx файл в фоне (celery)
- [X] Описать ручки в документации
- [ ] Добавить тесты для полного списка меню
- [ ] Добавить аутентификацию
