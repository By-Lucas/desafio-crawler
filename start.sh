#!/bin/sh

# Executar celery
celery -A config.celery beat --loglevel=INFO & \
celery -A config.celery worker --loglevel=INFO \

python run.py
