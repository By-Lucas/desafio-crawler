import os
from celery import Celery
from decouple import config
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beemon.settings')

DJANGO_ENVIRONMENT = config('DJANGO_ENVIRONMENT')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL_PROD')# if DJANGO_ENVIRONMENT == "prod" else os.getenv('CELERY_BROKER_URL_QA')

app = Celery('beemon', broker=os.getenv('CELERY_BROKER_URL_QA'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(result_expires=3600, 
                enable_utc=True,
                task_concurrency=5,
                worker_heartbeat=120,
                worker_prefetch_multiplier=10,
                timezone='America/Sao_Paulo', 
                )

app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# app.conf.beat_schedule = {
#     'teste_celery': {
#         'task': 'data_scrapy.tasks.teste_celery',
#         'schedule': crontab(hour=20, minute=59),
#         'args': (1, 2, 4),  # Exemplo de passagem de IDs (1, 2, 3)
#     },

# }


# Carrega automaticamente as tarefas de qualquer arquivo tasks.py em aplicativos Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)