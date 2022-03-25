from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from wom.forms import RecipeForm, InstructionForm, IngredientForm

from .models import Instruction, Recipe, Ingredient


def dashboard(request):
    return render(request, 'wom/dashboard.html')


def createrecipe(request, recipe_id=''):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        # parent_pk = recipe.pk
        recipe.pk = None
        recipe.creator = request.user
        recipe.parent_id = recipe_id
        recipe.pub_date = timezone.now()
    except:
        recipe = Recipe()

    print(recipe)
    if request.method == "POST":
        recipeform = RecipeForm(request.POST, instance=recipe)
        instructionforms = [InstructionForm(request.POST,
                                            prefix=str(x), instance=Instruction()) for x in range(0, 20)]
        ingredientforms = [IngredientForm(request.POST,
                                          prefix=str(x), instance=Ingredient()) for x in range(0, 10)]
        if recipeform.is_valid() and all([instrform.is_valid() for instrform in instructionforms]) and all([ingredientform.is_valid() for ingredientform in ingredientforms]):
            new_recipe = recipeform.save()
            # new_recipe.parent = parent_pk
            # new_recipe.save()
            for instrform in instructionforms:
                new_instruction = instrform.save(commit=False)
                new_instruction.recipe = new_recipe
                new_instruction.save()
            for ingrform in ingredientforms:
                new_ingredient = ingrform.save(commit=False)
                new_ingredient.recipe = new_recipe
                new_ingredient.save()
            return redirect(reverse('wom:recipelist'))
    else:
        recipeform = RecipeForm(instance=recipe)
        instructionforms = [InstructionForm(prefix=str(
            x), instance=Instruction()) for x in range(0, 20)]
        ingredientforms = [IngredientForm(prefix=str(
            x), instance=Ingredient()) for x in range(0, 10)]

    return render(request, 'wom/createrecipe.html', {
        'recipe_form': recipeform,
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
