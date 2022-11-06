#!/bin/bash

apt-get update
apt-get install postgresql-client -y
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
python manage.py migrate
python manage.py loaddb
python manage.py createsuperuser2 --noinput
python manage.py collectstatic --no-input
gunicorn api_yamdb.wsgi:application --bind 0:8000

exec "$@"