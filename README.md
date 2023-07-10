
# Разработка

## Установка зависимостей

Создать виртаульное окружение через pyenv:

```bash
$ cd case-actions
$ pyenv virtualenv 3.11 cashbox-server// создание виртуального окружения для проекта
$ pyenv local cashbox-server // активация виртуального окружения для текущей папки
```
Установить необходимые пакеты:

```bash
(cashbox-server)$ pip install -U setuptools pip pipenv // установка утилиты для работы с зависимостями
(cashbox-server)$ pipenv install  // установка основных зависимостей проекта
(cashbox-server)$ pipenv install --dev // установка dev-зависимостей проекта
```

Важно: 
перед запуском внутри Docker, нужно обязательно выполнить команду `pipenv install`, 
чтобы сформировался Pipfile.lock, именно из этого файла должна браться информация о зависимостях при сборке докер образа. 
Также необходимо добавить этот файл в индекс git-а.

## Запуск внутри Docker

```bash
$ docker-compose up
```

