#!/bin/bash

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddb
docker-compose exec web python manage.py createsuperuser2 --noinput
docker-compose exec web python manage.py collectstatic --no-input
