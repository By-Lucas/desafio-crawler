import uuid
import json
import datetime
from loguru import logger
from threading import Thread

from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_celery_beat.models import CrontabSchedule, PeriodicTask

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
                }
                return JsonResponse(data)
        
@login_required
def add_schedule(request):
    form = ScheduleForm(request.POST)
    if form.is_valid():
        company = form.cleaned_data['company']
        update_time = form.cleaned_data['update_time']
        _company = Company.objects.get(pk=company.pk)
        
        schedule = CrontabSchedule.objects.create(hour=update_time.hour, 
                                                minute=update_time.minute)
        
        task_uuid = uuid.uuid4()
        task = PeriodicTask.objects.create(crontab=schedule, 
                                        name=f'Mailing {_company.corporate_name} : {task_uuid}', 
                                        task='clippings.tasks.send_matters_company', 
                                        args=json.dumps([_company.id]))
        
        existing_schedules = SchedulingTask.objects.filter(company=_company, periodic_task=task, contrabe_scheduler=schedule).first()
        if existing_schedules:
            headers = {
                'status': 201,
                'HX-Trigger': json.dumps({
                    "list_schedulings": None,
                    'bg_color': 'bg-warning',
                    'showMessage': {
                        'message': f'Este agendamento já existe.',
                        'bgClass': 'warning'
                    }
                })
            }
            return HttpResponse(headers=headers)
        
        scheduling_tasks = SchedulingTask.objects.create(company=_company, 
                                                        periodic_task=task,
                                                        contrabe_scheduler=schedule)

        headers = {
            'status': 201,
            'HX-Trigger': json.dumps({
                "list_schedulings": None,
                'bg_color': 'bg-success',
                'showMessage': {
                    'message': f'Agendamento cadastrado com sucesso.',
                    'bgClass': 'success'
                }
            })
        }
        return HttpResponse(headers=headers)
       
    else:
        return render(request, 'company/includes/form-scheduling.html', {'form': form})


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
    template_name = "company/includes/modal-delete-schedule.html"
    schedule = get_object_or_404(SchedulingTask, pk=pk)
    schedule_celery = get_object_or_404(PeriodicTask, pk=schedule.periodic_task.pk)
    context = {}
    context['schedule']=schedule
    context['schedule_celery']=schedule_celery

    if request.method == "DELETE":
        if schedule and schedule_celery:
            schedule.delete()
            schedule_celery.delete()
            headers = {
                'status': 204,
                'HX-Trigger': json.dumps({
                    "list_schedulings": 'list_schedulings',
                    'bg_color': 'bg-success',
                    'showMessage': {
                        'message': f'Agendamento deletado com sucesso.',
                        'bgClass': 'success'
                    }
                })
            }
            return HttpResponse(headers=headers)
        else:
            headers = {
                    'status': 404,
                    'HX-Trigger': json.dumps({
                        "list_emails_mailings": None,
                        'bg_color': 'bg-danger',
                        'showMessage': {
                            'message': f'Erro: Agendamento não encontrado',
                            'bgClass': 'danger'}})}
            return HttpResponse(headers=headers)
    
    return render(request, template_name, context)