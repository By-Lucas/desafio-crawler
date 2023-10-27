from django.urls import path
from . import views

app_name = 'data_scrapy'

urlpatterns = [
    path('create', views.QuotesViews.as_view(), name='create_data'),
    path('scheduling', views.ScheduleView.as_view(), name='scheduling'),
    path('quotes-dataframe', views.QuotesDataframe.as_view(), name='quotes_dataframe'),
    
]