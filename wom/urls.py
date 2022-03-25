from django.urls import path, re_path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    re_path(r'^createrecipe/(?P<recipe_id>\d+)?',
            views.createrecipe, name='createrecipe'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),

]
