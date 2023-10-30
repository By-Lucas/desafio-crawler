#!/bin/sh
celery -A beemon worker --loglevel=INFO -Q update-tasks --concurrency=1 --without-gossip --without-mingle -O fair & \
celery -A beemon beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
python manage.py makemigrations && python manage.py migrate
gunicorn beemon.wsgi:application --bind 0.0.0.0:$PORT
