#!/bin/bash

# python manage.py migrate
# python manage.py loaddb
# python manage.py createsuperuser2 --noinput
# python manage.py collectstatic --no-input
gunicorn api_yamdb.wsgi:application --bind 0:8000

exec "$@"