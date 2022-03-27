# https://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from django.urls import reverse
# from wom.forms import RecipeForm, InstructionInlineFormset
# from wom.forms import RecipeForm, InstructionInlineFormset, IngredientInlineFormset, IngredientQuantityInlineFormset
from wom.forms import RecipeForm, InstructionForm, IngredientForm, IngredientForm1, InstructionForm1

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Recipe, FavoriteRecipe, Instruction, Ingredient
import operator
from functools import reduce
from wom.forms import RecipeForm, InstructionForm, IngredientForm, IngredientForm1, InstructionForm1

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')


# class createrecipe(generic.CreateView):
#     model = Recipe
#     fields = ['title', 'description', 'cooking_time',
#               'preparation_time', 'meal_type', 'course', 'pub_date']
#     template_name = 'wom/createrecipe.html'

#     def get_success_url(self):
#         return 'recipelist'

def createrecipe(request):
    if request.method == "POST":
        recipeform = RecipeForm(request.POST, instance=Recipe())
        instructionform1 = InstructionForm1(request.POST, instance=Instruction())
        ingredientform1 = IngredientForm1(request.POST, instance=Ingredient())

        instructionforms = [InstructionForm(request.POST,
                                            prefix=str(x), instance=Instruction()) for x in range(0, 19)]
        ingredientforms = [IngredientForm(request.POST,
                                          prefix=str(x), instance=Ingredient()) for x in range(0, 9)]
        # print('instructionform1 text field is currently', instructionform1.data['text'], "\n" )
        # print('instructionforms [0] text field is currently', instructionforms[0].data['text'], "\n" )
        # if recipeform.is_valid() and instructionform1.data['text'] != "" and ingredientform1.data['name'] != "" and ingredientform1.data['quantity'] != 0 and ingredientform1.data['units'] != "":
        if recipeform.is_valid() and instructionform1.is_valid() and ingredientform1.is_valid():
        # if recipeform.is_valid() and instructionforms[0].data['text'] != "" and ingredientforms[0].data['name'] != "" and ingredientforms[0].data['quantity'] != 0 and ingredientforms[0].data['units'] != "":
        # if recipeform.is_valid() and all([instrform.is_valid() for instrform in instructionforms]) and all([ingredientform.is_valid() for ingredientform in ingredientforms]):
            new_recipe = recipeform.save()
            new_instruction = instructionform1.save(commit=False)
            new_instruction.recipe = new_recipe
            new_instruction.save()
            for instrform in instructionforms:
                new_instruction = instrform.save(commit=False)
                new_instruction.recipe = new_recipe
                new_instruction.save()
            new_ingredient = ingredientform1.save(commit=False)
            new_ingredient.recipe = new_recipe
            new_ingredient.save()
            for ingrform in ingredientforms:
                new_ingredient = ingrform.save(commit=False)
                new_ingredient.recipe = new_recipe
                if(new_ingredient.quantity == ""):
                    new_ingredient.quantity = 0
                new_ingredient.save()
            return redirect(reverse('wom:recipelist'))
    else:
        recipeform = RecipeForm(instance=Recipe())
        instructionform1 = InstructionForm(instance=Instruction())
        ingredientform1 = IngredientForm(instance=Ingredient())
        instructionforms = [InstructionForm(prefix=str(x), instance=Instruction()) for x in range(0, 19)]
        ingredientforms = [IngredientForm(prefix=str(x), instance=Ingredient()) for x in range(0, 9)]
       
    return render(request, 'wom/createrecipe.html', {
        'recipe_form': recipeform,
        'instruction_form1': instructionform1,
        'ingredient_form1': ingredientform1,
        'instruction_forms': instructionforms,
        'ingredient_forms': ingredientforms,
    })


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
