from django.urls import path
from . import views

app_name = 'data_scrapy'

urlpatterns = [
    path('create', views.QuotesViews.as_view(), name='create_data'),
]