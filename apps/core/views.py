import json
import datetime
from loguru import logger
from datetime import timedelta

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from core.models import NotificationsModel


def home(requests):
    template_name = "core/home.html"
    return render(requests, template_name)

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