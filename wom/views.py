# https://www.youtube.com/watch?v=vU0VeFN-abU
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from wom.forms import IngredientFormset, InstructionFormset, RecipeForm, TagFormset, RequiredFormset, NotRequiredFormset


from .models import Recipe, FavoriteRecipe

from .models import Recipe, FavoriteRecipe, RateRecipe, Instruction, Ingredient, Tag
from django.db.models import Q
from django.http import HttpResponseRedirect
import operator
from functools import reduce
from django.utils import timezone
from datetime import timedelta

from django.forms import modelformset_factory


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
            new_recipe.creator = request.user
            # new_recipe.image = request.FILES.get('image')
            # print(request.FILES)
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

    filter_result = filter(request)
    post = filter_result['object_list']
    ingredients_search = filter_result['ingredients_search']
    tags_search = filter_result['tags_search']
    show_advanced_search = 'show' if filter_result['show_advanced_search'] else ''
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

    return render(request, template, {'object_list': post, "ingredients_search": ingredients_search, 'tags_search': tags_search, 'show_advanced_search': show_advanced_search})


def filter(request):
    q = Recipe.objects.all()
    message = ""
    filtered = False
    meal_type = request.GET.get('meal_type')
    course = request.GET.get('course')
    prep_time = request.GET.get('prep_time')
    cook_time = request.GET.get('cook_time')
    ingredients = request.GET.getlist('ingredients')
    tags = request.GET.getlist('tags')
    sort_by = request.GET.get('sort_by')

    for ingredient in ingredients:
        if ingredient == '' or ingredient is None or ingredient.isspace():
            ingredients.remove(ingredient)

    for tag in tags:
        if tag == '' or tag is None or tag.isspace():
            tags.remove(tag)

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
            t = timedelta(hours=1)
            q = q.filter(cooking_time__gte=t)
        else:
            times = cook_time.split(':')
            times = list(map(int, times))
            t = timedelta(hours=times[0], minutes=times[1], seconds=times[2])
            q = q.filter(cooking_time__lte=t)
        filtered = True
    if sort_by != '' and sort_by is not None:
        if sort_by == 'AZ':
            q = q.order_by('title')  # want to
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
    if ingredients != [] and ingredients is not None:
        for ingredient in ingredients:
            q = q.filter(ingredient__name__iexact=ingredient)
        filtered = True
    if tags != [] and tags is not None:
        for tag in tags:
            q = q.filter(tag__name__iexact=tag)
        filtered = True

    if filtered == False:
        q = Recipe.objects.all()

    return {'object_list': q, 'message': message, 'ingredients_search': ingredients, 'tags_search': tags, 'show_advanced_search': filtered}


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wom/detail.html'

    def get_context_data(self, **kwargs):
        """
        Creates an 'is_favorite' object that gets passed to the detail template if a
        Favorite object relating the logged-in user and the recipe being viewed exists.

        In the template, if the 'is_favorite' object exists, the "Save" button is
        replaced with an "Unsave" button.
        """
        context = super().get_context_data(**kwargs)
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_anonymous == 0:
            if self.request.user.favorites.filter(recipe=recipe).exists():
                context['is_favorite'] = {0}
            if self.request.user.rating.filter(recipe=recipe).exists():
                score = self.request.user.rating.get(recipe=recipe).score
                context['first_star'] = {0}
                if score >= 2:
                    context['second_star'] = {0}
                    if score >= 3:
                        context['third_star'] = {0}
                        if score >= 4:
                            context['fourth_star'] = {0}
                            if score >= 5:
                                context['fifth_star'] = {0}

        if recipe.avgRating > 0.25:
            context['0_5_avg'] = {0}
            if recipe.avgRating > 0.75:
                context['1_0_avg'] = {0}
                if recipe.avgRating > 1.25:
                    context['1_5_avg'] = {0}
                    if recipe.avgRating > 1.75:
                        context['2_0_avg'] = {0}
                        if recipe.avgRating > 2.25:
                            context['2_5_avg'] = {0}
                            if recipe.avgRating > 2.75:
                                context['3_0_avg'] = {0}
                                if recipe.avgRating > 3.25:
                                    context['3_5_avg'] = {0}
                                    if recipe.avgRating > 3.75:
                                        context['4_0_avg'] = {0}
                                        if recipe.avgRating > 4.25:
                                            context['4_5_avg'] = {0}
                                            if recipe.avgRating > 4.75:
                                                context['5_0_avg'] = {0}
        return context


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
    InstructionFormset = modelformset_factory(model=Instruction, formset=RequiredFormset,
                                              fields=('text',), extra=0)
    IngredientFormset = modelformset_factory(model=Ingredient, formset=RequiredFormset,
                                             fields=('name', 'quantity', 'units'), extra=0)
    TagFormset = modelformset_factory(
        model=Tag, formset=NotRequiredFormset, fields=('name',), extra=1)
    if request.method == "POST":
        recipeform = RecipeForm(
            request.POST, request.FILES, instance=recipe_to_update, prefix="recipe")
        instruction_formset = InstructionFormset(
            request.POST, prefix="instruction",)
        ingredient_formset = IngredientFormset(
            request.POST, prefix="ingredient",)
        tag_formset = TagFormset(
            request.POST, prefix="tag",)

        if (recipeform.is_valid() and instruction_formset.is_valid() and ingredient_formset.is_valid() and tag_formset.is_valid()):
            recipe_to_update = recipeform.save(commit=False)
            recipe_to_update.instruction_set.all().delete()
            recipe_to_update.ingredient_set.all().delete()
            recipe_to_update.tag_set.all().delete()

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
                print("new tag name", new_tag.name)
                if new_tag.name != "":
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
                    ((recipe.avgRating * recipe.numRatings) -
                     old_rating.score) / (recipe.numRatings - 1)

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
                ((recipe.avgRating * recipe.numRatings) -
                 existent_rating.score) / (recipe.numRatings - 1)

        recipe.avgRating = \
            ((recipe.avgRating * (recipe.numRatings - 1)) +
             rating) / (recipe.numRatings)

        existent_rating.score = rating
        recipe.save()
        existent_rating.save()

    else:
        """ 
        Case 3: create a new rating object relating user, score, and recipe,
        then update average rating and number of ratings accordingly
        """
        new_rating = RateRecipe.objects.create(
            user=request.user, recipe=recipe, score=rating)

        recipe.avgRating = \
            ((recipe.avgRating * recipe.numRatings) +
             rating) / (recipe.numRatings + 1)

        recipe.numRatings += 1
        new_rating.save()
        recipe.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
