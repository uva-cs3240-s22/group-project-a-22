from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template('wom/dashboard.html')
    return HttpResponse(template.render({}, request))