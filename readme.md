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


Переходим на сайт
http://127.0.0.1:8000/

Для Er диаграммы
![QuickDBD-export](ER.jpg)

# Проект Lyceum


[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/172792-mario12526-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/172792-mario12526-course-1187/-/commits/main)