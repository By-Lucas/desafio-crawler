import json
import datetime
from loguru import logger
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from import_export.admin import ImportExportModelAdmin
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
