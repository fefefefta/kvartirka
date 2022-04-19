#!/bin/sh

sleep 10

python manage.py flush --no-input
python manage.py makemigrations blog
python manage.py migrate

exec "$@"
