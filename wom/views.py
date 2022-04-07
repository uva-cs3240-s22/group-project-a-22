from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
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

    if request.method == 'GET':
        search = request.GET.get('q')
        if (not search or search.isspace() or search == ""):
            post = Recipe.objects.all()
        else:
            search_keywords = search.split()
            q = reduce(operator.and_, (Q(title__icontains=kw)
                       for kw in search_keywords))
            post = Recipe.objects.filter(q)
    else:
        post = Recipe.objects.all()
    return render(request, template, {'object_list': post})


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
