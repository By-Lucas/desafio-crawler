import asyncio
from loguru import logger
from threading import Thread

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, View

from data_scrapy.models import ScrapyQuotesModel
from helpers.scraper_quotes import ScraperQuotes
from core.models import NotificationsModel as notify


scrapy = ScraperQuotes()


class QuotesViews(View):
    
    async def get(self, request):
        # Implemente o código para o método GET aqui
        return JsonResponse({'message': 'GET method'})

    async def post(self, request):
        context = {}
        
        def handle_scrapy():
            scrapy__ = scrapy.run()
            if scrapy__:
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
                    if create:
                        logger.success('Dados atualizados com sucesso')
                        
                    notify.objects.create(title="Dados atualizados com sucesso", 
                                        description="Os dados raspadaos do site quotes foram atualizados com sucesso.")
                    
                except ScrapyQuotesModel.DoesNotExist:
                    logger.error('A model ScrapyQuotesModel não existe ou ainda não foi criada')
        
        thread = Thread(target=handle_scrapy)
        thread.start()
        thread.join(1)
        
        context['status'] = 200,
        context['message'] = 'Os dados serão atualizados em segundo plano. Em breve receberá uma noficicação informando.',
        return JsonResponse(context)
