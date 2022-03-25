from django import forms
from .models import Recipe, Instruction, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'creator', 'description', 'cooking_time',
                  'preparation_time', 'meal_type', 'course']
        help_texts = {
            'cooking_time': 'Example format for a 1.5 hour cooking time: 1:30:00',
            'preparation_time': 'Example format for a 5 minute preparation time: 5:00',
        }


class InstructionForm(forms.ModelForm):
    text = forms.CharField(required=False)

    class Meta:
        model = Instruction
        fields = ['text']


class IngredientForm(forms.ModelForm):
    name = forms.CharField(required=False)
    quantity = forms.CharField(required=False)
    units = forms.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'units']
