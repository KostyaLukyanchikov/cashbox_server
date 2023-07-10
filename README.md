
## Установка зависимостей

Создать виртуальное окружение через pyenv:

```bash
$ cd cashbox_server
$ pyenv virtualenv 3.11 cashbox-server// создание виртуального окружения для проекта
$ pyenv local cashbox-server // активация виртуального окружения для текущей папки
```
Установить необходимые пакеты:

```bash
(cashbox-server)$ pip install -U setuptools pip pipenv // установка утилиты для работы с зависимостями
(cashbox-server)$ pipenv install  // установка основных зависимостей проекта
(cashbox-server)$ pipenv install --dev // установка dev-зависимостей проекта
```

## База данных
Создать базу данных, добавить в нее таблицы из create_tables.sql

Настроить параметры подключений в config.yaml

## Запуск внутри Docker

```bash
$ docker-compose up
```

# Тест
При успешном запуске, на главой странице откроется страница со swagger

