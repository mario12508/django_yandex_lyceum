# Проект Lyceum

[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/172792-mario12526-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/172792-mario12526-course-1187/-/commits/main)

## Запуск проекта в режиме разработки

### Шаг 1: Установка и активация виртуального окружения

Устанавливаем виртуальное окружение:
```commandline
python -m venv venv
```

Активируем его:
- Для Linux/macOS:
    ```
    source venv/bin/activate
    ```
- Для Windows:
    ```
    venv\Scripts\activate
    ```

### Шаг 2: Установка зависимостей

Создаем папку `requirements`, создаем там файлы `test.txt`, `dev.txt` и `prod.txt` 
и устанавливаем зависимости:
```commandline
pip install -r requirements/test.txt
```

### Шаг 3: Настройка переменных окружения

Создайте файл `.env.template` с содержимым:
```
SECRET_KEY='your-secret-key' 
DEBUG=True
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
DJANGO_ALLOW_REVERSE=False
```

После этого создайте файл `.env` на основе шаблона:
```
cp .env.template .env
```

Настройте в файле `.env` секретный ключ и другие переменные.

### Шаг 4: Запуск проекта

Перейдите в папку с файлом `manage.py`:
```
cd <название_проекта>
```

Запускаем сервер разработки:
```commandline
python manage.py runserver
```

### Шаг 5: Открытие проекта

Откройте проект в браузере по адресу:
```
http://127.0.0.1:8000/
```

### Шаг 6: создание миграций и фикстур
Если вы внесли изменения в модели, то сначала создайте миграции:
```commandline
python manage.py makemigrations
```
затем сделайте миграцию:
```commandline
python manage.py migrate
```
после чего вы можете загрузить данные для БД из фикстур:
```commandline
python manage.py loaddata fixtures/data.json
```
для созданий фикстур используйте:
```commandline
python -Xutf8 manage.py dumpdata catalog -o fixtures/data.json
```

### Шаг 7: тестирование проекта:
Если вы хотите протестировать ваш проект введите следующую команду
```commandline
python manage.py test
```
но перед этим пропишите тесты в файлах `tests.py` в приложениях

### Шаг 8: создание директории статистических файлов
В своём проекте рядом с `templates` создайте `static_dev`, куда 
вы можете загрузить изображения, css, js и прочие статические файлы.

После этого в файле `settings.py` создайте переменную:
```commandline
STATIC_URL = "static/"
```
и
```commandline
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]
```
а в самих `.html` файлах пишите, например:
```commandline
{% load static %}
...
<img src="{% static 'my_app/example.jpg' %}" alt="My image">
```

# Развёртывание проекта с учётом локализации

## Локализация

Проект поддерживает локализацию с использованием встроенных возможностей Django. Чтобы добавить новые переводы:

1. Создайте файл перевода с помощью команды:
    ```bash
    django-admin makemessages -l <your_language_code>
    ```

2. Отредактируйте файл `.po`, добавив переводы.

3. Скомпилируйте переводы с помощью команды:
    ```bash
    django-admin compilemessages
    ```

## Добавление текущего года в футер

Текущий год автоматически добавляется в футер с учетом часовых поясов и отключенного JavaScript. В случае, если JavaScript отключен, используется серверное время.

### ER Диаграмма

![QuickDBD-export](ER.jpg)
