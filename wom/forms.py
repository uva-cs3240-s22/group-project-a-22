from mimetypes import init
from django import forms
from .models import Recipe, Instruction, Ingredient


class RecipeForm(forms.ModelForm):
    anonymous_creator_bool = forms.BooleanField(label="Anonymous Creator", required=False, initial=False, help_text= 'If you wish this recipe to have an anonymous creator, check this box. Otherwise, your username will be used.')
    # creator = forms.CheckboxInput(help_text= 'Please specify your public creator name if you do not want it to be \'Anonymous\'')
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time',
                  'preparation_time', 'meal_type', 'course', 'anonymous_creator_bool']
        help_texts = {
            'cooking_time': 'Example format for a 1.5 hour cooking time: 1:30:00',
            'preparation_time': 'Example format for a 5 minute preparation time: 5:00',
        }


class InstructionForm(forms.ModelForm):
    text = forms.CharField(label="", required=False)
    class Meta:
        model = Instruction
        fields = ['text']

class InstructionForm1(forms.ModelForm):
    text = forms.CharField(label="")
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

class IngredientForm1(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'units']
