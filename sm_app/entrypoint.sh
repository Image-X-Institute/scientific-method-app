#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py flush --no-input
python manage.py makemigrations
python3 manage.py migrate

if [ "$DJANGO_SUPERUSER_EMAIL" ]
then
  python manage.py createsuperuser \
    --noinput \
    --email $DJANGO_SUPERUSER_EMAIL \
    --name $DJANGO_SUPERUSER_NAME
fi

exec "$@"
