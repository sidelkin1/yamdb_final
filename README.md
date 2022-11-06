![yamdb workflow](https://github.com/sidelkin1/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# API Yamdb
Проект YaMDb собирает отзывы пользователей на различные произведения.

Реализован бэкенд проекта и `REST API` для него.

## Установка и запуск проекта

Клонировать репозиторий:

```
git clone https://github.com/sidelkin1/infra_sp2.git

```

Cоздать и запустить контейнеры:

```
cd infra_sp2/infra

docker-compose up -d --build
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate

```

Заполнить базу данных:

```
docker-compose exec web python manage.py loaddb
```

Собрать всю статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Для удаления контейнеров выполнить команду:

```
cd infra_sp2/infra

docker-compose down -v
```

## Примеры запросов к API

Для регистрации пользователя и получения токена необходимо сделать запрос с `json` телом  
```
{
    "email": "string",
    "username": "string"
}
```
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
После этого в папке `sent_emails` будет создано письмо с кодом подтверждения, который нужно отправить в формате
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/token/
```

Получение списка всех произведений
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Добавление нового отзыва к произведению.
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полный перечень запросов к API можно получить по эндпоинту `redoc`
```
http://127.0.0.1:8000/redoc
```

## Шаблон ENV-файла

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

## Используемые технологии
```
Python 3.7, Django 2.2 (django rest framework + simplejwt), Docker
```

## Авторы
[Константин Сидельников](https://github.com/sidelkin1)
