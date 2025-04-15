#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn webapp.wsgi:application --bind 0.0.0.0:8000
