from django.urls import path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
