from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

# Create your views here.
def members(request):
    print(Member.objects.all().values())
    context = {
        'mymembers': Member.objects.all().values(),
    }
    template = loader.get_template('first.html')
    return HttpResponse(template.render(context, request))

def details(request, id):
    member = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': member
    }
    return HttpResponse(template.render(context, request))