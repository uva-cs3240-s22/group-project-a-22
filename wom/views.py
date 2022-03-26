from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
# from wom.forms import RecipeForm, InstructionInlineFormset
# from wom.forms import RecipeForm, InstructionInlineFormset, IngredientInlineFormset, IngredientQuantityInlineFormset
from wom.forms import RecipeForm, InstructionForm, IngredientForm

from .models import Instruction, Recipe, Ingredient

# https://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.db.models import Q

from .models import Recipe
import operator
from functools import reduce

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')


def createrecipe(request):
    if request.method == "POST":
        recipeform = RecipeForm(request.POST, instance=Recipe())
        instructionforms = [InstructionForm(request.POST,
                                            prefix=str(x), instance=Instruction()) for x in range(0, 20)]
        ingredientforms = [IngredientForm(request.POST,
                                          prefix=str(x), instance=Ingredient()) for x in range(0, 10)]
        # if recipeform.is_valid():
        if recipeform.is_valid() and all([instrform.is_valid() for instrform in instructionforms]) and all([ingredientform.is_valid() for ingredientform in ingredientforms]):
            new_recipe = recipeform.save()
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
        recipeform = RecipeForm(instance=Recipe())
        instructionforms = [InstructionForm(prefix=str(x), instance=Instruction()) for x in range(0, 20)]
        ingredientforms = [IngredientForm(prefix=str(x), instance=Ingredient()) for x in range(0, 10)]
       
    return render(request, 'wom/createrecipe.html', {
        'recipe_form': recipeform,
        'instruction_forms': instructionforms,
        'ingredient_forms': ingredientforms,
    })


# class createrecipe(generic.CreateView):
#     model = Recipe
#     form_class = RecipeForm
#     template_name = 'wom/createrecipe.html'
#     def get_context_data(self, **kwargs):
#         context = super(createrecipe, self).get_context_data(**kwargs)
#         context['instruction_formset'] = InstructionInlineFormset()
#         context['ingredient_quantity_formset'] = IngredientQuantityInlineFormset()
#         # context['ingredient_formset'] = IngredientInlineFormset()
#         context['ingredient_form'] = IngredientForm()
#         return context
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         instruction_formset = InstructionInlineFormset(self.request.POST)
#         ingredient_quantity_formset = IngredientQuantityInlineFormset(self.request.POST)
#         # ingredient_formset = IngredientInlineFormset(self.request.POST)
#         ingredient_form = IngredientForm(self.request.POST)
#         # if form.is_valid() and instruction_formset.is_valid() and ingredient_quantity_formset.is_valid() and ingredient_formset.is_valid():
#         # if form.is_valid() and instruction_formset.is_valid() and ingredient_quantity_formset.is_valid() and ingredient_form.is_valid():
#         if form.is_valid() and instruction_formset.is_valid() and ingredient_quantity_formset.is_valid():
#         # if form.is_valid() and instruction_formset.is_valid():
#             return self.form_valid(form, instruction_formset, ingredient_quantity_formset, ingredient_form)
#             # return self.form_valid(form, instruction_formset, ingredient_quantity_formset, ingredient_formset)
#             # return self.form_valid(form, instruction_formset)
#         else:
#             return self.form_invalid(form, instruction_formset, ingredient_quantity_formset, ingredient_form)
#             # return self.form_invalid(form, instruction_formset, ingredient_quantity_formset, ingredient_formset)
#             # return self.form_invalid(form, instruction_formset)

#     def form_valid(self, form, instruction_formset, ingredient_quantity_formset, ingredient_formset):
#     # def form_valid(self, form, instruction_formset):
#         self.object = form.save(commit = False)
#         self.object.save()
#         instructions = instruction_formset.save(commit = False)
#         for instruction in instructions:
#             print('instruction.recipe beforebond', instruction.recipe)
#             instruction.recipe = self.object
#             print("instruction.recipe after saving is now", instruction.recipe)
#             instruction.save()
#         ingredients= ingredient_formset.save(commit = False)
#         ingredientQuantities = ingredient_quantity_formset.save(commit = False)
#         for ingredientQuantity in ingredientQuantities:
#             # for ingredient in ingredients:
#                 # ingredient.save()
#                 # ingredientQuantity.ingredient = ingredient
#             ingredientQuantity.save()
#         return redirect('/wom/recipelist')

#     def form_invalid(self, form, instruction_formset, ingredient_quantity_formset, ingredient_formset):
#     # def form_invalid(self, form, instruction_formset):
#         return self.render_to_response(
#             self.get_context_data(form=form, instruction_formset=instruction_formset, ingredient_quantity_formset=ingredient_quantity_formset, ingredient_formset=ingredient_formset)
#         )


#     def get_success_url(self):
#         return 'recipelist'
#         # return render(request, 'wom/recipelist.html')
#     # return HttpResponse('recipelist/html')


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


def favorite_recipe(request, id):
    """
    Currently unused, but this code will run when the favorite button is pressed once we have a favorite button
    """
    recipe = get_object_or_404(Recipe, id)
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else :
        recipe.favorites.add(request.user)
    return redirect('', pk=pk)


class favoritelist(generic.ListView):
    template_name = 'wom/favoritelist.html'

    def get_queryset(self):
        """
        Returns the favorited recipes of the user who is logged in
        """
        user = self.request.user
        return user.favorites.all()

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
