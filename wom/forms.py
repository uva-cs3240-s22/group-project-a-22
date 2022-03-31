from mimetypes import init
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
    class Meta:
        model = Instruction
        fields = ['text']


InstructionFormset = forms.formset_factory(
    InstructionForm, extra=3, can_delete=False)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'units']


IngredientFormset = forms.formset_factory(IngredientForm, extra=3)
