from django.urls import path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('createrecipe/<int:id>/',
         views.createrecipe.as_view(), name='createrecipe'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),

]
