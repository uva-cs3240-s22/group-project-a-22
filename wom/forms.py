from logging import PlaceHolder
from random import choices
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Instruction, Ingredient, IngredientQuantity

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'preparation_time', 'meal_type', 'course']
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=1000)
    cooking_time = forms.DurationField(help_text="Example format for a 1.5 hour cooking time: 1:30:00")
    preparation_time = forms.DurationField(help_text="Example format for a 5 minute preparation time: 5:00")
    meal_type = forms.ChoiceField(
        choices=Recipe.MealTypes.choices)
    # meal_type = forms.ChoiceField(
    #     max_length=10, choices=Recipe.mealTypes.choices, default=Recipe.MealTypes.OTHER)
    # course = forms.ChoiceField(
    #     choices=Meta.model.Courses)
    course = forms.ChoiceField(
        choices=Recipe.Courses.choices)
    # # modelchoicefield in django tutorial for ingredients & instructions 
    # inline formsets 

    InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=('text',))
    formset = InstructionFormSet(instance=None)
    