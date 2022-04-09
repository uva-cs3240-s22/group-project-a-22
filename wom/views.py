from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from wom.forms import IngredientFormset, InstructionFormset, RecipeForm
from .models import Recipe, FavoriteRecipe

from .models import Recipe, FavoriteRecipe, RateRecipe, Instruction, Ingredient
from django.db.models import Q
from django.http import HttpResponseRedirect
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


def dashboard(request):
    return render(request, 'wom/dashboard.html')


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
    """
    Runs when the favorite button is pressed on the Details page.
    Takes recipe ID (pk) and request.

    Creates a new favorite object relating the user who made the request to the recipe
    with the passed pk. If such an object already exists, deletes that object instead.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.favorites.filter(user=request.user).exists():
        recipe.favorites.filter(user=request.user).delete()
    else:
        new_favorite = FavoriteRecipe.objects.create(
            user=request.user, recipe=recipe)
        new_favorite.save()
    return redirect(request.META['HTTP_REFERER'])


class favoritelist(generic.ListView):
    template_name = 'wom/favoritelist.html'

    def get_queryset(self):
        """
        Returns the favorited recipes of the user who made the request
        """
        user = self.request.user
        return user.favorites.all()


def rate_recipe(request, pk, rating):
    """
    Runs when the favorite button is pressed on the Details page.
    Takes recipe ID (pk) and request.

    Creates a new rating object relating the user who made the request and the score they gave
    to the recipe with the passed pk. If such an object already exists, deletes that object instead.
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if rating == 6:
        """ 
        Case 1: delete rating if it exists (and rating == 6),
        then update average rating and number of ratings accordingly

        The rating will never be 6 under normal circumstances, so this is just a shortcut
        for testing and potentially for implementing a "remove rating" button if we want that.
        """
        if recipe.rating.filter(user=request.user).exists():
            old_rating = recipe.rating.get(user=request.user)

            if recipe.numRatings == 1:
                recipe.avgRating = 0
            else:
                recipe.avgRating = \
                    ((recipe.avgRating * recipe.numRatings) - old_rating.score) / (recipe.numRatings - 1)

            recipe.numRatings -= 1
            old_rating.delete()
            recipe.save()

    elif recipe.rating.filter(user=request.user).exists():
        """ 
        Case 2: change an existent rating to a new score,
        then update average rating accordingly
        
        Does not change number of ratings (obviously).
        
        This basically just runs the calculation for removing a rating with the user's 
        old score, then the calculation for adding a rating with the user's new score.
        """
        existent_rating = recipe.rating.get(user=request.user)

        if recipe.numRatings == 1:
            recipe.avgRating = 0
        else:
            recipe.avgRating = \
                ((recipe.avgRating * recipe.numRatings) - existent_rating.score) / (recipe.numRatings - 1)

        recipe.avgRating = \
            ((recipe.avgRating * (recipe.numRatings-1)) + rating) / (recipe.numRatings)

        existent_rating.score = rating
        recipe.save()
        existent_rating.save()

    else:
        """ 
        Case 3: create a new rating object relating user, score, and recipe,
        then update average rating and number of ratings accordingly
        """
        new_rating = RateRecipe.objects.create(user=request.user, recipe=recipe, score=rating)

        recipe.avgRating = \
            ((recipe.avgRating * recipe.numRatings) + rating) / (recipe.numRatings+1)

        recipe.numRatings += 1
        new_rating.save()
        recipe.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
