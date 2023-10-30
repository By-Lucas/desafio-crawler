from loguru import logger
from celery import shared_task

from helpers.scraper_quotes import ScraperQuotes
from data_scrapy.models import ScrapyQuotesModel
from core.models import NotificationsModel as notify
#from beemon.celery import app


@shared_task(max_retries=3, queue='update-tasks', default_retry_delay=1)
def update_data():
    logger.success('Iniciando atualização de dados agendada')
    
    scrapy = ScraperQuotes()
    scrapy__ = scrapy.run()
    if scrapy:
        try:
            for data in scrapy__:
                create, update = ScrapyQuotesModel.objects.update_or_create(
                    title=data['text'],
                    author=data['Author'],
                    defaults={
                        'tags':data['Tags'],
                        'born':data['Born'],
                        'location':data['Location'],
                        'description':data['Description'],
                    }
                )
            
            logger.success('Dados atualizados com sucesso')
            notify.objects.create(title="Dados atualizados com sucesso", 
                                    description="Os dados raspadaos do site quotes foram atualizados com sucesso.")

        except ScrapyQuotesModel.DoesNotExist:
            logger.error('A model ScrapyQuotesModel não existe ou ainda não foi criada')
            raise Exception('A model ScrapyQuotesModel não existe ou ainda não foi criada')