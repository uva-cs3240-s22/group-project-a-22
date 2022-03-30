from django.urls import path, re_path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    re_path(r'^createrecipe/(?P<recipe_id>\d+)?',
            views.createrecipe, name='createrecipe'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),
    path('favoritelist', views.favoritelist.as_view(), name='favoritelist'),
    path('fav/<int:pk>', views.favorite_recipe, name='fav'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.RecipeView.as_view(), name='detail'),

]