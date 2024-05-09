# Bet Maker

Описание

## Локальное окружение

Подготовка локального окружения:

1. Установка всех зависимостей

```shell
pip install -r requirements.txt
pip install -r requirements-test.txt
pip install -r requirements-dev.txt
```

2. Установка pre-commit хуков

```shell
pre-commit install
```

### Выполнение проверок перед каждым коммитом

Перед каждым git commit [pre-commit](https://pre-commit.com/) выполняет следующие действия:

- Удаление ненужных пробелов
- Добавление пустой строки в конце файла
- Запуск [code-style проверок](#проверка-code-style)
- Запуск [тестов](#запуск-тестов)

В случае неуспешного прохождения проверок коммит не будет создан.

Конфигурация pre-commit находится в файле [.pre-commit-config.yaml](.pre-commit-config.yaml).

Чтобы выполнить проверку вручную можно вызвать команду:

```shell
pre-commit run --all-files
```

### Проверка code-style

Проверка code-style происходит с помощью утилиты `Ruff`.
Конфигурация находится в [pyproject.toml](pyproject.toml). Подробнее про настройку можно прочесть
в [документации Ruff](https://docs.astral.sh/ruff/configuration/).

Для запуска проверки code-style требуется выполнить команду:

```shell
ruff check .
```

### Запуск тестов

Тесты написаны на базе фреймворка `pytest`. Конфигурация находится в [pyproject.toml](pyproject.toml). Тесты расположены
в директории [tests](tests).

Для запуска тестов требуется выполнить команду:

```shell
python -m pytest
```

## Production окружение

**Dockerfile** и **docker-compose** файлы лежат в директории [deployment](deployment).

### Переменные окружения

| Переменная окружения | Описание                          | Значение по умолчанию                                  |
|----------------------|-----------------------------------|--------------------------------------------------------|
| DB_DATABASE          | Название базы данных              | bet-maker                                              |
| DB_USER              | Имя пользователя базы данных      | test                                                   |
| DB_PASSWORD          | Пароль пользователя базы данных   | test                                                   |
| DB_PORT              | Порт базы данных                  | 6432                                                   |
| DB_DSN               | DSN для подключения к базе данных | postgresql+asyncpg://test:test@database:6432/scheduler |

### Миграция для базы данных

Установить переменные окружения в терминале и выполнить скрипт для установки миграций.

```shell
alembic upgrade head
```