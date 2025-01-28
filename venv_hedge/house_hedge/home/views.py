from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def handler404(request, error):
    print("hah")
    template = loader.get_template('404.html')
    context = {
        'request': request
    }
    
    return HttpResponse(template.render())