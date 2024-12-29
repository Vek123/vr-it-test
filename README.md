# vr-it-test
## Инструкция по запуску
* Локальный запуск:
  1) Скачать репозиторий => Распаковать.
  2) Создать виртуальное окружение: `python -m venv .venv`
  3) Устиновить зависимости: `pip install -r requirements.txt`
  4) Создать файл `.env` в корне проекта и заполнить его данными по примеру из файла `.env_example`
  5) Запустить проект: `python main.py`
  6) Запустить тесты: `pytest`
  7) Применить миграции: `alembic upgrade head`
  8) Проверить доступ к документации по адресу: http://localhost:8000/docs. Или Ваш порт, указанный в файле `.env`
* Запуск через docker-compose
  1) Скачать файл `docker-compose.yml` или скопировать его содержимое в свой файл.
  2) Создать файл `.env` и заполнить его по примеру из файла `.env_example`. `docker-compose.yml` и `.env` должны находиться в одной папке. В переменной окружения `REDIS_HOST` должно быть значение: `redis`, если файл `docker-compose.yml` не изменялся.
  3) Запустить контейнер: `docker-compose up`
  4) Запустить тесты: `docker-compose exec app pytest`
  5) Применить миграции: `docker-compose exec app alembic upgrade head`
  6) Проверить доступ к документации по адресу: http://localhost:8000/docs. Или Ваш порт, указанный в файле `.env`