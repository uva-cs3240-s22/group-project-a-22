from django.urls import path

from . import views

app_name = 'wom'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('createrecipe', views.createrecipe.as_view(), name='createrecipe'),
    path('recipelist', views.recipelist.as_view(), name='recipelist'),
    path('favoritelist', views.favoritelist.as_view(), name='favoritelist'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.RecipeView.as_view(), name='detail'),

]
