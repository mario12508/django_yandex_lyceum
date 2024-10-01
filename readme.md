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

pipeline
stages:
  - linting

flake8:
  stage: linting
  image: registry.gitlab.com/pipeline-components/flake8:latest
  script:
    - pip install -r requirements.txt
    - flake8 --verbose


Переходим на сайт
http://127.0.0.1:8000/
