from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def singin(request):
    template = loader.get_template('singin.html')
    return HttpResponse(template.render())

def singup(request):
    template = loader.get_template('singup.html')
    return HttpResponse(template.render())

def reset_password(request):
    template = loader.get_template('reset_password.html')
    return HttpResponse(template.render())
