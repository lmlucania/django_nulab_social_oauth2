#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
if [ $DEBUG = True ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn config.wsgi:application
fi