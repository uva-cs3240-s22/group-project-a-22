from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic
from wom.forms import RecipeForm, InstructionInlineFormset 

# from wom.forms import RecipeForm, InstructionInlineFormset, IngredientForm, IngredientQuantityInlineFormset
from django.contrib import messages 
from django.urls import reverse

from .models import Recipe

def dashboard(request):
    return render(request, 'wom/dashboard.html')

# def createrecipe(request):
#     model = Recipe
#     return render(request, 'wom/createrecipe.html')

class createrecipe(generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'wom/createrecipe.html' 
    def get_context_data(self, **kwargs):
        context = super(createrecipe, self).get_context_data(**kwargs)
        context['instruction_formset'] = InstructionInlineFormset()
        # context['ingredient_quantity_formset'] = IngredientQuantityInlineFormset()
        # context['ingredient_form'] = IngredientForm()
        return context
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instruction_formset = InstructionInlineFormset(self.request.POST)
        # ingredient_quantity_formset = IngredientQuantityInlineFormset(self.request.POST)
        # ingredient_form = IngredientForm(self.request.POST)
        # if form.is_valid() and instruction_formset.is_valid() and ingredient_quantity_formset.is_valid() and ingredient_form.is_valid():
        if form.is_valid() and instruction_formset.is_valid():
            # return self.form_valid(form, instruction_formset, ingredient_quantity_formset, ingredient_form)
            return self.form_valid(form, instruction_formset)
        else:
            # return self.form_invalid(form, instruction_formset, ingredient_quantity_formset, ingredient_form)
            return self.form_invalid(form, instruction_formset)
    
    # def form_valid(self, form, instruction_formset, ingredient_quantity_formset, ingredient_formset):
    def form_valid(self, form, instruction_formset):
        self.object = form.save(commit = False)
        self.object.save()
        instructions = instruction_formset.save(commit = False)
        for instruction in instructions:
            print('instruction.recipe beforebond', instruction.recipe)
            instruction.recipe = self.object
            print("instruction.recipe after saving is now", instruction.recipe)
            instruction.save()
        # ingredients= ingredient_formset.save(commit = False)
        # ingredientQuantities = ingredient_quantity_formset.save(commit = False)
        # for ingredient in ingredients:
        #     for ingredientQuantity in ingredientQuantities:
        #         ingredientQuantity.ingredient = ingredient
        #         ingredientQuantity.save()
        #     ingredient.save()
        return redirect('/wom/recipelist')

    # def form_invalid(self, form, instruction_formset, ingredient_quantity_formset, ingredient_formset):
    def form_invalid(self, form, instruction_formset):
        return self.render_to_response(
            self.get_context_data(form=form, instruction_formset=instruction_formset)
        )
        

    def get_success_url(self):
        return 'recipelist'
        # return render(request, 'wom/recipelist.html')
    # return HttpResponse('recipelist/html')


class recipelist(generic.ListView):
    template_name = 'wom/recipelist.html' 
    def get_queryset(self):
        """
        Return the published recipes
        """
        return Recipe.objects.all()
