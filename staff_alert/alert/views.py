from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView

class Index(TemplateView):

    template_name = 'index.html'

def input(request):

    return  HttpResponse("<a href = 'output/'>input</a>")


def output(request):

    return  HttpResponse("<a href = 'input/'>output</a>")

# Create your views here.
