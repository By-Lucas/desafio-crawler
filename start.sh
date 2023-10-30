#!/bin/sh

# Executar celery
celery -A apps.config.celery beat --loglevel=INFO & \
celery -A apps.config.celery worker --loglevel=INFO \

python run.py
