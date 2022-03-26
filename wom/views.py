# https://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.db.models import Q

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Recipe, FavoriteRecipe
import operator
from functools import reduce

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')


class createrecipe(generic.CreateView):
    model = Recipe
    fields = ['title', 'description', 'cooking_time',
              'preparation_time', 'meal_type', 'course', 'pub_date']
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
        if (search.isspace()) or (search == ""):
            post = Recipe.objects.all()
        else:
            search_keywords = search.split()
            q = reduce(operator.and_, (Q(title__contains = kw) for kw in search_keywords))
            post = Recipe.objects.filter(q)
            print(post)
    else:
        post = Recipe.objects.all()
    return render(request, template, {'post': post})


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wom/detail.html'


def favorite_recipe(request, pk):
    """
    Currently unused, but this code will run when the favorite button is pressed once we have a favorite button
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.favorites.filter(user=request.user).exists():
        recipe.favorites.filter(user=request.user).delete()
    else:
        newfavorite = FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        newfavorite.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class favoritelist(generic.ListView):
    template_name = 'wom/favoritelist.html'

    def get_queryset(self):
        """
        Returns the favorited recipes of the user who is logged in
        """
        user = self.request.user
        return user.favorites.all()
