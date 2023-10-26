from django.shortcuts import render


def home(requests):
    template_name = "core/home.html"
    return render(requests, template_name)