from logging import PlaceHolder
from random import choices
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Instruction, Ingredient, IngredientQuantity


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time',
                  'preparation_time', 'meal_type', 'course']
        help_texts = {
            'cooking_time': 'Example format for a 1.5 hour cooking time: 1:30:00',
            'preparation_time': 'Example format for a 5 minute preparation time: 5:00'
        }


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['text']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class IngredientQuantityForm(forms.ModelForm):
    class Meta:
        model = IngredientQuantity
        fields = ['ingredient', 'quantity', 'units']
    # ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all())
    # quantity = forms.FloatField()
    # units = forms.CharField(max_length=5)
