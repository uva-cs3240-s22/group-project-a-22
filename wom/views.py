# https://www.youtube.com/watch?v=vU0VeFN-abU
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
# from matplotlib.contour import ContourSet
from wom.forms import IngredientFormset, InstructionFormset, RecipeForm
from .models import Recipe, FavoriteRecipe

from django.db.models import Q
import operator
from functools import reduce
from django.utils import timezone

# def createrecipe(request, recipe_id=''):
#     try:
#         recipe = Recipe.objects.get(pk=recipe_id)
#         # parent_pk = recipe.pk
#         recipe.pk = None
#         recipe.creator = request.user
#         recipe.parent_id = recipe_id
#         recipe.pub_date = timezone.now()
#     except:
#         recipe = Recipe()


def createrecipe(request, recipe_id=''):
    if not request.user.is_authenticated:
        return render(request, 'wom/createrecipe.html')

    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.parent_id = recipe_id
    except:
        recipe = Recipe()

    instruction_query_set = recipe.instruction_set.all()
    ingredient_query_set = recipe.ingredient_set.all()
    recipe.creator = request.user
    recipe.pub_date = timezone.now()
    if request.method == "POST":
        recipeform = RecipeForm(
            request.POST, instance=recipe, prefix="recipe")
        instruction_formset = InstructionFormset(
            request.POST, prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            request.POST, prefix="ingredient", queryset=ingredient_query_set)
        if recipeform.is_valid() and instruction_formset.is_valid() and ingredient_formset.is_valid():
            new_recipe = recipeform.save(commit=False)
            new_recipe.pk = None
            new_recipe.save()
            for instrform in instruction_formset:
                new_instruction = instrform.save(commit=False)
                new_instruction.pk = None
                new_instruction.recipe = new_recipe
                new_instruction.save()
            for ingrform in ingredient_formset:
                new_ingredient = ingrform.save(commit=False)
                new_ingredient.pk = None
                new_ingredient.recipe = new_recipe
                new_ingredient.save()
            return redirect(reverse('wom:search'))
    else:
        recipeform = RecipeForm(instance=recipe, prefix="recipe")
        instruction_formset = InstructionFormset(
            prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            prefix="ingredient", queryset=ingredient_query_set)

    return render(request, 'wom/createrecipe.html', {
        'recipe_form': recipeform,
        'instruction_forms': instruction_formset,
        'ingredient_forms': ingredient_formset,
    })


def search(request):
    template = "wom/search_results.html"

    post = filter(request)['object_list']
    if request.method == 'GET':
        search = request.GET.get('q')
        if (not search or search.isspace() or search == ""):
            post = post
        else:
            search_keywords = search.split()
            q = reduce(operator.and_, (Q(title__icontains=kw)
                       for kw in search_keywords))
            post = post.filter(q)
    else:
        post = Recipe.objects.all()
    return render(request, template, {'object_list': post.order_by('title')})


def filter(request):
    q = Recipe.objects.all()
    message = ""
    filtered = False
    meal_type = request.GET.get('meal_type')
    course = request.GET.get('course')
    prep_time = request.GET.get('prep_time')
    cook_time = request.GET.get('cook_time')
    sort_by = request.GET.get('sort_by')

    if meal_type != '' and meal_type is not None:
        q = q.filter(meal_type__iexact=meal_type)
        filtered = True
    if course != '' and course is not None:
        q = q.filter(course__iexact=course)
        filtered = True
    if prep_time != '' and prep_time is not None:
        if prep_time == '1:00:01': 
            t = timedelta(hours=1)
            q = q.filter(preparation_time__gte=t)
        else:
            times = prep_time.split(':')
            times = list(map(int, times))
            t = timedelta(hours=times[0], minutes=times[1], seconds=times[2])
            q = q.filter(preparation_time__lte=t)
        filtered = True
    if cook_time != '' and cook_time is not None:
        if cook_time == '1:00:01':
            t = timedelta( hours=1)
            q = q.filter(cooking_time__gte=t)
        else: 
            times = cook_time.split(':')
            times = list(map(int, times))
            t = timedelta( hours=times[0], minutes=times[1], seconds=times[2] )
            q = q.filter(cooking_time__lte=t)
        filtered = True   
    if sort_by != '' and sort_by is not None:
        if sort_by == 'AZ':
            q = Recipe.objects.all().order_by('title') #want to
        elif sort_by == 'Recent':
            q = Recipe.objects.all().order_by('-pub_date')
        elif sort_by == 'Oldest':
            q = Recipe.objects.all().order_by('pub_date')
        filtered = True
    if filtered == False:
        print('not filtered')
        q = Recipe.objects.all() 

    
    return {'object_list': q, 'message': message}
    



class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wom/detail.html'


def favorite_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.favorites.filter(user=request.user).exists():
        recipe.favorites.filter(user=request.user).delete()
    else:
        newfavorite = FavoriteRecipe.objects.create(
            user=request.user, recipe=recipe)
        newfavorite.save()
    return redirect(request.META['HTTP_REFERER'])


class favoritelist(generic.ListView):
    template_name = 'wom/favoritelist.html'

    def get_queryset(self):
        """
        Returns the favorited recipes of the user who is logged in
        """
        user = self.request.user
        return user.favorites.all()
