from django.urls import path
from data_scrapy import views

app_name = 'data_scrapy'

urlpatterns = [
    path('create', views.QuotesViews.as_view(), name='create_data'),
    path('scheduling', views.ScheduleView.as_view(), name='scheduling'),
    path('delete-scheduling/<int:pk>', views.delete_schedule, name='delete_schedule'),
    path('quotes-dataframe', views.QuotesDataframe.as_view(), name='quotes_dataframe'),
    path('download/<str:format>/', views.download_data, name='download_data'),
]