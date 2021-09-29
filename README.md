# Продуктовый помощник

http://drunkbrush.ru/

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

Для тестов (админ):
```
username = aizi
email = aizi@aizi.ru
password = aizi
```

Онлайн-сервис и API для него.

На этом сервисе пользователи могут публиковать рецепты.

Подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное».

А перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Развертка проекта в Docker
1. Клонируем репозиторий 
```
git clone https://github.com/nightriddler/foodgram-project-react.git
```
2. В папке `infra` с проектом создаем файл `.env` с переменными окружения:
```
SECRET_KEY=django-insecure-lafmj3e24%et%ku0(&x8)yd7bn^0ibhnjwdf6*mhjoz&n=gl)^
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
3. В этой же папке `infra` запускаем docker-compose командой 
```
docker-compose up
```
После этой команды развернётся проект, запущенный через `gunicorn` с базой данных `postgres`.
> Во время работы контейнеров в терминале ведётся лог, и выполнить из этого терминала команды невозможно. Придётся открыть второй терминал, перейти в папку с проектом и выполнять следующие команды оттуда.

4. В корне проекта делаем миграции и собираем статику
```
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --noinput
```
5. Создаем супер пользователя
```
docker-compose exec web python manage.py createsuperuser
```
6. Заполняем базу начальными данными (ингредиентами)
```
docker-compose exec web python manage.py loaddata fixtures/ingredients.json
```
7. Проект доступен по адресу
```
http://127.0.0.1/
```
8. Чтобы тэги для рецептов были доступны их необходимо добавить через панель администратора
```
http://127.0.0.1/admin/recipes/tag/
```
## Документация
В `/docs/openapi-schema.yml` доступна документация в формате Redoc. 

Удобно посмотреть можно тут - https://editor.swagger.io/ 

## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)