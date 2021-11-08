# Продуктовый помощник

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Задача и описание

К фронтенду (одностраничное приложение на React), написать онлайн-сервис и API для него.
На этом сервисе пользователи могут публиковать рецепты.
Подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное».
А перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым). Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

![2021-09-29_19-36-14](https://user-images.githubusercontent.com/75097575/135312804-85f2e59f-3753-462f-81bb-690918d8559d.png)

>При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате показаны рецепты, которые отмечены хотя бы одним из этих тегов.
При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. Такой же принцип соблюдается при фильтрации списка избранного.

### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

![2021-09-29_19-58-43](https://user-images.githubusercontent.com/75097575/135315039-0dacb4f6-a6d1-42be-bf7b-24f217cc3756.png)

### Создание рецепта
При создании рецепта все поля обязательны к заполнению. Тэги выбираются из заранее предустановленных.

![2021-09-29_19-36-57](https://user-images.githubusercontent.com/75097575/135312832-3859c9c9-d410-4305-9877-b1c8a2f74aa6.png)
>Валидация осуществляется по количеству ингредиента (не меньше 1) и времени приготовления (не меньше 0).

### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

![2021-09-29_19-36-41](https://user-images.githubusercontent.com/75097575/135312860-11c12a71-0f92-4938-99c0-a203ece9de19.png)

### Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

![2021-09-29_19-37-53](https://user-images.githubusercontent.com/75097575/135312879-13371f7c-9cb0-4a04-b277-c97d4f02ea32.png)

### Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

![2021-09-29_19-38-30](https://user-images.githubusercontent.com/75097575/135312897-a9984caf-bde8-4b6f-8c0a-474b6e1c3627.png)

Список покупок скачивается в формате `.txt`

Одинаковые ингредиенты суммируются, список сортируется по убыванию количества (без учета единицы измерения. 

![2021-09-29_19-46-17](https://user-images.githubusercontent.com/75097575/135313120-60c920ff-25c0-4cf8-99e9-6439460ed8ff.png)


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

![2021-09-29_19-14-10](https://user-images.githubusercontent.com/75097575/135312922-9e9329ba-fbcd-4f4f-9eeb-600147e742ed.png)

## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)
