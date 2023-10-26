from typing import Any
from django import http
from django.shortcuts import render

from django.views.generic.base import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic.edit import CreateView, UpdateView, View



class QuotesViews(CreateView):
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        
        print('POST funcionando', request.POST),
        headers = {
            'status': 201,
            'message': f'Criado'}
        return JsonResponse(headers)