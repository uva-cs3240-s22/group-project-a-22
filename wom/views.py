from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def index(request):
    return HttpResponse('This is the index page.')


def login(request):
    return render(request, 'wom/googleAPI.html')
