# https://www.youtube.com/watch?v=vU0VeFN-abU
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from wom.forms import IngredientFormset, InstructionFormset, RecipeForm, TagFormset


from .models import Recipe, FavoriteRecipe

from .models import Recipe, FavoriteRecipe, RateRecipe, Instruction, Ingredient
from django.db.models import Q
from django.http import HttpResponseRedirect
import operator
from functools import reduce
from django.utils import timezone
from datetime import timedelta

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
    tag_query_set = recipe.tag_set.all()
    recipe.creator = request.user
    recipe.pub_date = timezone.now()
    if request.method == "POST":
        recipeform = RecipeForm(
            request.POST, request.FILES, instance=recipe, prefix="recipe")
        instruction_formset = InstructionFormset(
            request.POST, prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            request.POST, prefix="ingredient", queryset=ingredient_query_set)
        tag_formset = TagFormset(
            request.POST, prefix="tag", queryset=tag_query_set)
        if recipeform.is_valid() and instruction_formset.is_valid() and ingredient_formset.is_valid() and tag_formset.is_valid():
            new_recipe = recipeform.save(commit=False)
            # if(new_recipe.anonymous_creator_bool == True):
            #     new_recipe.creator = None
            # else:
            #     new_recipe.creator = request.user
            new_recipe.creator = request.user
            # new_recipe.image = request.FILES.get('image')
            #print(request.FILES)
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
            for tag in tag_formset:
                new_tag = tag.save(commit=False)
                new_tag.pk = None
                new_tag.recipe = new_recipe
                new_tag.save()
            return redirect(reverse('wom:search'))
    else:
        recipeform = RecipeForm(instance=recipe, prefix="recipe")
        instruction_formset = InstructionFormset(
            prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            prefix="ingredient", queryset=ingredient_query_set)
        tag_formset = TagFormset(prefix="tag", queryset=tag_query_set)

    return render(request, 'wom/createrecipe.html', {
        'recipe_form': recipeform,
        'instruction_forms': instruction_formset,
        'ingredient_forms': ingredient_formset,
        'tag_forms': tag_formset,
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
    return render(request, template, {'object_list': post})


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
            print('prep time less than 30 min')
            times = prep_time.split(':')
            times = list(map(int, times))
            t = timedelta(hours=times[0], minutes=times[1], seconds=times[2])
            q = q.filter(preparation_time__lte=t)
        filtered = True
    if cook_time != '' and cook_time is not None:
        if cook_time == '1:00:01':
            print('cook time more than an hr')
            t = timedelta(hours=1)
            q = q.filter(cooking_time__gte=t)
            print('greater than')
        else: 
            print('prep time less than')
            times = cook_time.split(':')
            times = list(map(int, times))
            t = timedelta( hours=times[0], minutes=times[1], seconds=times[2] )
            q = q.filter(cooking_time__lte=t)
        filtered = True   
    if sort_by != '' and sort_by is not None:
        if sort_by == 'AZ':
            q = q.order_by('title') #want to
        elif sort_by == 'Recent':
            q = q.order_by('-pub_date')
        elif sort_by == 'Oldest':
            q = q.order_by('pub_date')
        elif sort_by == 'Highest':
            q = q.order_by('-avgRating')
        elif sort_by == 'Highest_Week':
            week_ago = datetime.now(tz=timezone.utc) - timedelta(days=7)
            q = q.filter(pub_date__gte=week_ago).order_by('-avgRating')
        elif sort_by == 'Highest_Month':
            month_ago = datetime.now(tz=timezone.utc) - timedelta(days=30)
            q = q.filter(pub_date__gte=month_ago).order_by('-avgRating')
        elif sort_by == 'Highest_Year':
            year_ago = datetime.now(tz=timezone.utc) - timedelta(days=365)
            q = q.filter(pub_date__gte=year_ago).order_by('-avgRating') 
        filtered = True
    if filtered == False:
        q = Recipe.objects.all() 

    
    return {'object_list': q, 'message': message}
    



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


def childrenlist(request, pk):
    template = "wom/childrenlist.html"

    q = Recipe.objects.filter(parent=get_object_or_404(Recipe, pk=pk))

    return render(request, template, {'object_list': q})


# def filter(request):
#     template = "wom/search_results.html"
    
#     q = Recipe.objects.all()
#     filtered = False
#     meal_type = request.GET.get('meal_type')
#     course = request.GET.get('course')
#     prep_time = request.GET.get('prep_time')
#     cook_time = request.GET.get('cook_time')

#     if meal_type != '' and meal_type is not None:
#         q = q.filter(meal_type__iexact=meal_type)
#         filtered = True
#     if course != '' and course is not None:
#         q = q.filter(course__iexact=course)
#         filtered = True
#     if prep_time != '' and prep_time is not None:
#         if prep_time == '1:00:01': 
#             t = timedelta(hours=1)
#             q = q.filter(preparation_time__gte=t)
#         else:
#             times = prep_time.split(':')
#             times = list(map(int, times))
#             t = timedelta(hours=times[0], minutes=times[1], seconds=times[2])
#             q = q.filter(preparation_time__lte=t)
#         filtered = True
#     if cook_time != '' and cook_time is not None:
#         if cook_time == '1:00:01':
#             t = timedelta( hours=1)
#             q = q.filter(cooking_time__gte=t)
#         else: 
#             times = cook_time.split(':')
#             times = list(map(int, times))
#             t = timedelta( hours=times[0], minutes=times[1], seconds=times[2] )
#             q = q.filter(cooking_time__lte=t)
#         filtered = True
       
#     if filtered == False:
#         q = Recipe.objects.none() 

#     return render(request, template, {'object_list': q})

def account(request):
    template = "wom/account.html"
    return render(request, template, {'object_list': Recipe.objects.all})

def delete_recipe(request, recipe_id=''):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect(reverse('wom:account'))

def update_recipe(request, recipe_id=''):
    recipe_to_update = Recipe.objects.get(pk=recipe_id)
    template = 'wom/updaterecipe.html'

    instruction_query_set = recipe_to_update.instruction_set.all()
    ingredient_query_set = recipe_to_update.ingredient_set.all()
    tag_query_set = recipe_to_update.tag_set.all()
    recipe_to_update.pub_date = timezone.now()
    if request.method == "POST":
        recipeform = RecipeForm(
            request.POST, request.FILES, instance=recipe_to_update, prefix="recipe")
        instruction_formset = InstructionFormset(
            request.POST, prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            request.POST, prefix="ingredient", queryset=ingredient_query_set)
        tag_formset = TagFormset(
            request.POST, prefix="tag", queryset=tag_query_set)
        if recipeform.is_valid() and instruction_formset.is_valid() and ingredient_formset.is_valid() and tag_formset.is_valid():
            recipe_to_update = recipeform.save(commit=False)
            recipe_to_update.creator = request.user
            
            recipe_to_update.save()
            for instrform in instruction_formset:
                new_instruction = instrform.save(commit=False)
                new_instruction.recipe = recipe_to_update
                new_instruction.save()
            for ingrform in ingredient_formset:
                new_ingredient = ingrform.save(commit=False)
                new_ingredient.recipe = recipe_to_update
                new_ingredient.save()
            for tag in tag_formset:
                new_tag = tag.save(commit=False)
                new_tag.recipe = recipe_to_update
                new_tag.save()
            return redirect(reverse('wom:account'))
    else:
        recipeform = RecipeForm(instance=recipe_to_update, prefix="recipe")
        instruction_formset = InstructionFormset(
            prefix="instruction", queryset=instruction_query_set)
        ingredient_formset = IngredientFormset(
            prefix="ingredient", queryset=ingredient_query_set)
        tag_formset = TagFormset(prefix="tag", queryset=tag_query_set)

    return render(request, template, {
        'recipe_form': recipeform,
        'instruction_forms': instruction_formset,
        'ingredient_forms': ingredient_formset,
        'tag_forms': tag_formset,
    })


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
