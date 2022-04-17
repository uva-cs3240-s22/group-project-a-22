from django.shortcuts import redirect
from django.urls import path, re_path, include

from . import views

app_name = 'wom'
urlpatterns = [
    path('', lambda request: redirect('search/')),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.RecipeView.as_view(), name='detail'),
    path('rate/<int:pk>/<int:rating>', views.rate_recipe, name='rate'),
    path('fav/<int:recipe_id>', views.favorite_recipe, name='fav'),
    path('favoritelist', views.favoritelist.as_view(), name='favoritelist'),
    path('<int:pk>/children', views.childrenlist, name='childrenlist'),
    path('account', views.account, name='account'),
    re_path(r'^createrecipe/(?P<recipe_id>\d+)?',
            views.createrecipe, name='createrecipe'),
    path('delete-recipe/<int:recipe_id>',
         views.delete_recipe, name='delete-recipe'),
    path('update-recipe/<int:recipe_id>',
         views.update_recipe, name='update-recipe')
]
