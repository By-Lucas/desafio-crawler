import os
import sys
import configparser
from loguru import logger
from decouple import config

from celery import Celery, shared_task
from celery.schedules import crontab

from bot.helpers.scraper_quotes import ScraperQuotes


logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini')

HOUR = config_ini['CONFIG']['UPDATE_HOUR']
MINUTES = config_ini['CONFIG']['UPDATE_MINUTES']


CELERY_BROKER_URL = config('CELERY_BROKER_URL')

print(CELERY_BROKER_URL)
app = Celery('beemon', broker=CELERY_BROKER_URL)
app.conf.update(result_expires=3600, 
                enable_utc=True,
                task_concurrency=5,
                worker_heartbeat=120,
                worker_prefetch_multiplier=10,
                timezone='America/Sao_Paulo', 
                )

@shared_task(max_retries=3, queue='update-tasks', default_retry_delay=1)
def scrape_quotes():
    logger.success("Scraping agendado iniciado")
    url = config("URL_QUOTES")
    scraper = ScraperQuotes(url)
    data = scraper.run_scraper(save_json=True, save_xlsx=True, quantity_page=2)
    logger.info("Scraping agendado completo")
    return data


# @shared_task
# def scrape_data():
#     logger.success("Scraping agendado iniciado")
#     url = config("URL_QUOTES")
#     scraper = ScraperQuotes(url)
#     data = scraper.run_scraper(save_json=True, save_xlsx=True, quantity_page=2)
#     logger.info("Scraping agendado completo")
#     return data


app.conf.beat_schedule = {
    'update_data': {
        'task': 'config.celery.scrape_quotes',  # Atualize para o caminho correto da sua tarefa
        'schedule': crontab(hour=15, minute=25),
        'args': (),  # Exemplo de passagem de IDs (1, 2, 3)
    },
    'update_datas': {
        'task': 'config.celery.scrape_quotes',  # Atualize para o caminho correto da sua tarefa
        'schedule': crontab(hour=15, minute=27),
        'args': (),  # Exemplo de passagem de IDs (1, 2, 3)
    },
}

