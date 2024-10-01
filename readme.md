Запуск проекта в dev-режиме

устанавливаем виртуальное окружение:
pip install venv
Запускаем его:
python -m venv venv
активируем его:
source venv/bin/activate

создаем requirements.txt
pip install -r requirements.txt

настройка секретного ключа и окружения 
echo SECRET_KEY="your secret key" >> .env
echo DEBUG=True >> .env

переходим в папку с manage.py
cd <название проекта>

запускаем сервер
python manage.py runserver

Создайте файл .env в корне проекта и добавьте туда настройки, например:
SECRET_KEY='your-secret-key'
DEBUG=True

pipeline
stages:
  - linting

lint_quotes:
  stage: linting
  image: python:3.9
  script:
    - pip install flake8 flake8-quotes
    - flake8
  only:
    - main


Переходим на сайт
http://127.0.0.1:8000/
