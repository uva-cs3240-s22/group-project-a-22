from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from wom.forms import RecipeForm

from .models import Recipe

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')

class createrecipe(generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    # fields = '__all__'
    # fields = ['title', 'description', 'cooking_time', 'preparation_time', 'meal_type', 'course', 'pub_date']
    template_name = 'wom/createrecipe.html' 

    # def form_valid(self, form):
    #     form.save()
    #     return super(Recipe, self).form_valid(form)
    def get_success_url(self):
        return 'recipelist'

class recipelist(generic.ListView):
    template_name = 'wom/recipelist.html' 
    def get_queryset(self):
        """
        Return the published recipes
        """
        return Recipe.objects.all()
