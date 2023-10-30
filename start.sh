#!/bin/sh

# Executar o Celery worker
celery -A config.celery worker --loglevel=INFO &

# Executar o Celery Beat
celery -A config.celery beat --loglevel=INFO &

# Executar o Python script (substitua "run.py" pelo nome do seu script)
python run.py
