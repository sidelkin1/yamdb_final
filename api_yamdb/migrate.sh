#!/bin/bash

python manage.py migrate
python manage.py loaddb
python manage.py createsuperuser2 --noinput
python manage.py collectstatic --no-input
