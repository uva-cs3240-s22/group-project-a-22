from django.shortcuts import redirect
from django.urls import path, re_path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),
    path('rate/<int:pk>/<int:rating>', views.rate_recipe, name='rate'),
    path('', lambda request: redirect('search/')),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.RecipeView.as_view(), name='detail'),
    re_path(r'^createrecipe/(?P<recipe_id>\d+)?',
            views.createrecipe, name='createrecipe'),
    path('favoritelist', views.favoritelist.as_view(), name='favoritelist'),
    path('fav/<int:recipe_id>', views.favorite_recipe, name='fav'),

]
