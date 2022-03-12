from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def dashboard(request):
    return render(request, 'wom/dashboard.html')
