import os
import uuid
import json
import datetime
import pandas as pd
from loguru import logger
from threading import Thread

from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule

from .forms import ScheduleForm
from data_scrapy.models import ScrapyQuotesModel
from helpers.scraper_quotes import ScraperQuotes
from core.models import NotificationsModel as notify


scrapy = ScraperQuotes()


class QuotesViews(CreateView):

    def post(self, request):
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


class QuotesDataframe(View):
    template_name = "core/includes/quotes-dataframe.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'data': []})
        
    def post(self, request, *args, **kwargs):
        quotes_data = 'media/quotes_data.xlsx'
        try:
            if os.path.isfile(quotes_data):
                dataframe = pd.read_excel(quotes_data).to_dict(orient='records')
                logger.success('Upload realizado com sucesso.')
            else:
                scrapy__ = scrapy.run(save_xlsx=True)
                dataframe = scrapy.show_dataframe().to_dict(orient='records')
                
                logger.success('Dados atualizados com sucesso.')
                notify.objects.create(title="Dados atualizados com sucesso", 
                                description="Os dados raspados do site quotes foram atualizados com sucesso")
                
            # Truncate the "Description" column to 80 characters and add '...' if needed
            for entry in dataframe:
                if 'Description' in entry and len(entry['Description']) > 80:
                    entry['Description'] = entry['Description'][:77] + '...'
                
                if 'text' in entry and len(entry['text']) > 40:
                    entry['text'] = entry['text'][:40] + '...'

            return JsonResponse({'dataframe': dataframe})
            
        except ScrapyQuotesModel.DoesNotExist:
            logger.error('A model ScrapyQuotesModel não existe ou ainda não foi criada')
            return JsonResponse({'dataframe': [],' message':'A models ScrapyQuotesModel ainda não existe, por favor crie-a antes de atualizar'})


def download_data(request, format):
    file_format = format
    # Fetch your data from the database or use the existing DataFrame
    queryset = ScrapyQuotesModel.objects.all()
    news_data = pd.DataFrame(list(queryset.values()))
    
    date_now = datetime.datetime.now()
    date_now = date_now.strftime('%d-%m-%Y')

    if file_format not in ['xlsx', 'csv', 'json']:
        return HttpResponse(status=400)

    date_now = datetime.date.today()
    date_now = date_now.strftime("%d-%m-%Y")
    name_download = f"quotes_data_{date_now}"

    if file_format == 'xlsx':
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename="{name_download}.xlsx'
        news_data.to_excel(response, index=False, engine="openpyxl")

    if file_format == 'csv':
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename="{name_download}.csv'
        news_data.to_csv(response, index=False)

    if file_format == 'json':
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = f'attachment; filename="{name_download}.json'
        response.write(news_data.to_json(orient="records"))

    return response
    

class ScheduleView(View):
    
    def get(self, request, *args, **kwargs):
        sidebar_config = True
        active_schedule_view = True
        
        form = ScheduleForm()
        schedulings = PeriodicTask.objects.filter(enabled=True)
        context = {
            'form':form,
            'schedulings': schedulings,
            'sidebar_config':sidebar_config,
            'active_schedule_view':active_schedule_view
            
        }
        return render(request, 'data_scrapy/list-schedule.html', context)
    
    def post(self, request, *args, **kwargs):
        update_time = request.POST.get('update_time', "")
            
        form = ScheduleForm(request.POST)
        if form.is_valid():
            update_time = form.cleaned_data['update_time']
            schedule = CrontabSchedule.objects.create(hour=update_time.hour, 
                                                minute=update_time.minute)

            task_uuid = uuid.uuid4()
            task = PeriodicTask.objects.create(crontab=schedule, 
                                        name=f'Atualizar tarefa : {task_uuid}', 
                                        task='data_scrapy.tasks.update_data')
            
            if task:
                data = {
                'status': 201,
                'message': 'Tarefa agendada com sucesso.',
                'schedule': {
                    'name': task.name,
                    'hour': task.crontab.hour,
                    'minutes': task.crontab.minute,
                    'enabled': task.enabled,
                    'task': task.task,
                    'pk': task.pk,
                }
            }
                #return JsonResponse(data)
        else:
            if not update_time:
                data = {
                        'status': 500,
                        'message': 'Por favor informe um horário válido',
                    }
        return JsonResponse(data)
            

@login_required
def edit_schedule(request, pk):
    schedule = get_object_or_404(SchedulingTask, pk=pk)
    schedule_celery = get_object_or_404(PeriodicTask, pk=schedule.periodic_task.pk)
    schedule_contrab = get_object_or_404(CrontabSchedule, pk=schedule.contrabe_scheduler.pk)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            update_time = form.cleaned_data['update_time']
            _company = Company.objects.get(pk=company.pk)

            # Atualize os objetos em vez de excluí-los
            schedule.company = _company
            schedule.save()

            # Aqui, estou assumindo que update_time é uma instância de datetime.time
            schedule_contrab.hour = update_time.hour
            schedule_contrab.minute = update_time.minute
            schedule_contrab.save()

            schedule_celery.args = json.dumps([_company.id])
            schedule_celery.crontab = schedule_contrab
            schedule_celery.save()

            headers = {
                'status': 201,
                'HX-Trigger': json.dumps({
                    "list_schedulings": None,
                    'bg_color': 'bg-success',
                    'showMessage': {
                        'message': f'Agendamento atualizado com sucesso.',
                        'bgClass': 'success'
                    }
                })
            }
            return HttpResponse(headers=headers)
    else:
        form = ScheduleForm(initial={
            'company': schedule.company,
            'update_time': datetime.time(hour=int(schedule_celery.crontab.hour), 
                                         minute=int(schedule_celery.crontab.minute)
                                        ),
        })

    return render(request, 'company/includes/edit-schedule.html', {'form': form})


def delete_schedule(request, pk):
    schedule_celery = get_object_or_404(PeriodicTask, pk=pk)
    
    if request.method == "DELETE":
        data = {}
        if schedule_celery:
            if schedule_celery.crontab:
                schedule_celery.crontab.delete()
            schedule_celery.delete()
            
            updated_schedules = PeriodicTask.objects.all()

            # Serialize the updated list of schedules
            if updated_schedules:
                datas = [{"name": schedule.name, "hour": schedule.crontab.hour, 'minutes': schedule.crontab.minute,  'enabled':schedule.enabled, 'task': schedule.task, "pk": schedule.pk} for schedule in updated_schedules]
                data = {'schedules': datas, 'message':'Agendamento deletado com sucesso.', 'status':204}
                
        else:
            data = {
                'status': 204,
                'schedules': [],
                'message': f'Agendamento não encontrado'
            }
        return JsonResponse(data)
    