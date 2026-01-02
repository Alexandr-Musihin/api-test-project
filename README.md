# api-test-project
# Petstore API Autotests

![API Tests](https://github.com/Alexandr-Musihin/api-test-project/workflows/api-tests.yml/badge.svg)

Проект автоматизации тестирования Petstore API (https://petstore.swagger.io).

## Структура проекта
api-test-project/
├── tests/ # Тесты разбиты по уровням сложности
│ ├── conftest.py # Фикстуры Pytest
│ ├── test_pet_crud.py # Базовые CRUD тесты (Уровень 1)
│ ├── test_pet_advanced.py # Продвинутые тесты (Уровень 2)
│ └── test_pet_pro.py # Профессиональные тесты (Уровень 3)
├── api/ # API клиент и модели
│ ├── client.py # HTTP клиент для работы с API
│ ├── models.py # Pydantic модели данных
│ └── schemas.py # JSON схемы для валидации
├── data/ # Тестовые данные
│ └── test_data.yaml # Данные для параметризации
├── .github/workflows/ # CI/CD конфигурация
└── requirements.txt # Зависимости Python

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/petstore-api-tests.git
cd petstore-api-tests
```
