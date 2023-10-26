from django.shortcuts import render


def home(requests):
    template_name = "home.html"
    return render(requests, template_name)