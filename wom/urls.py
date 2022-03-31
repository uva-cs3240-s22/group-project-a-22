from django.urls import path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('createrecipe', views.createrecipe, name='createrecipe'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),
    path('favoritelist', views.favoritelist.as_view(), name='favoritelist'),
    path('fav/<int:pk>', views.favorite_recipe, name='fav'),
    path('rate/<int:pk>/<int:rating>', views.rate_recipe, name='rate'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.RecipeView.as_view(), name='detail'),

]