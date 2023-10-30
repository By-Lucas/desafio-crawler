#!/bin/sh

# Executar celery
celery -A beemon worker --loglevel=INFO -Q update-tasks --concurrency=1 --without-gossip --without-mingle -O fair & \
celery -A beemon beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler & \

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Aplicar as migrações do banco de dados
python manage.py migrate

# Iniciar o servidor Gunicorn
gunicorn beemon.wsgi:application --bind 0.0.0.0:8080
#--bind 0.0.0.0:$PORT