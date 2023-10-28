from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('view-log/', views.view_log, name='view_log'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
]