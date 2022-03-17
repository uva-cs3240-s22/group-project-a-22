from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.db.models import Q

from .models import Recipe

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')

class createrecipe(generic.CreateView):
    model = Recipe
    fields = ['title', 'description', 'cooking_time', 'preparation_time', 'meal_type', 'course', 'pub_date']
    template_name = 'wom/createrecipe.html' 
    def get_success_url(self):
        return 'recipelist'

class recipelist(generic.ListView):
    template_name = 'wom/recipelist.html' 
    def get_queryset(self):
        """
        Return the published recipes
        """
        return Recipe.objects.all()

def search(request):
    template = "wom/search_results.html"
    
    if request.method == 'GET':
        search = request.GET.get('q')
        post = Recipe.objects.filter(Q(title__icontains=search))
        print(post)
    else:
        post = Recipe.objects.all()    
    return render(request, template, {'post' : post})

class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wom/detail.html'
    