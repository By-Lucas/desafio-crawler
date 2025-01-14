import os
import json
from loguru import logger
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from core.models import NotificationsModel
from data_scrapy.models import ScrapyQuotesModel


def home(requests):
    template_name = "core/home.html"
    data_scrapy = ScrapyQuotesModel.objects.all()
    notify = NotificationsModel.objects.all()
    
    context = {
        'data_scrapy':data_scrapy.order_by('-created_date'),
        'data_scrapy_quantity':data_scrapy.count(),
        'data_scrapy_lasted':notify.order_by('-created_date').first(),
        'notify_quantity':notify.count(),
        'tasks_celery_quantity': PeriodicTask.objects.filter(enabled=True).count()
    }
    return render(requests, template_name, context)


def get_quotes_data(request):
    data_scrapy_list = []
    notifications_list = []
    
    notify = NotificationsModel.objects.all()
    data_scrapy = ScrapyQuotesModel.objects.all()
    
    for data in data_scrapy:
        data_scrapy_list.append({
            'title': data.title,
            'author': data.author,
            'born': data.born,
            'location': data.location,
            'tags': data.tags,
            'description': data.description,
        })
    
        
    for notification in notify:
        notifications_list.append({
            'title': notification.title,
            'created_date': (notification.created_date - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        })
    
    context = {
        'notify_quantity': notify.count(),
        'data_scrapy': data_scrapy_list,
        'data_scrapy_lasted': notifications_list,
        'data_scrapy_quantity': data_scrapy.count(),
        'tasks_celery_quantity': PeriodicTask.objects.filter(enabled=True).count()
    }
    
    return JsonResponse(context)


def get_notifications(request):
    data = {}
    try:
        notify_ago = timezone.now() - timedelta(minutes=5)
        
        notify = NotificationsModel.objects.filter(is_active=True)
        notify.filter(created_date__lt=notify_ago).update(is_active=False)
        notifications = notify.order_by('-created_date')
        num_notifications = notifications.count()
                
        notifications_list = []
        
        for notification in notifications:
            notifications_list.append({
                'title': notification.title,
                'created_date': (notification.created_date - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
            })
        
        data['notifications'] = notifications_list
        data['num_notifications'] = num_notifications
        
    except NotificationsModel.DoesNotExist:
        data['notifications'] = []
        data['num_notifications'] = 0
    
    return JsonResponse(data)


@csrf_exempt
def view_log(request):
    log_file_path = 'logs/logs.log'  # Provide the correct path to your log file
    if os.path.isfile(log_file_path):
        try:
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.read()
        except FileNotFoundError:
            log_content = "Log file not found"
        
        return HttpResponse(log_content, content_type='text/plain')
    else:
        return JsonResponse({'status':500, 'message':'Arquivo de logs ainda não existe'})