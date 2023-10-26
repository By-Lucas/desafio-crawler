from django.contrib import admin

# from import_export.admin import ImportExportModelAdmin
# from django_celery_beat.admin import PeriodicTaskAdmin
# from django_celery_beat.models import PeriodicTask, IntervalSchedule

from data_scrapy.models import ScrapyQuotesModel


class ScrapyQuotesAdmin(admin.ModelAdmin):
    search_fields = ['author', 'created_date']
    list_display = ['author', 'created_date']
    list_filter = ('is_active',)
admin.site.register(ScrapyQuotesModel, ScrapyQuotesAdmin)


