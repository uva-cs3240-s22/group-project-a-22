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
    
    course = forms.ChoiceField(
        choices=Recipe.Courses.choices)
    
class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['text',]
    text = forms.CharField(max_length=500)


InstructionInlineFormset = inlineformset_factory(
    Recipe,
    Instruction,
    form=InstructionForm,
    extra=20,
)

class IngredientQuantityForm(forms.ModelForm):
    class Meta:
        model = IngredientQuantity
        fields = ['quantity', 'units']
    quantity = forms.FloatField()
    units = forms.CharField(max_length=5)

IngredientQuantityInlineFormset = inlineformset_factory(
    Ingredient,
    IngredientQuantity,
    form=IngredientQuantityForm,
)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name',]
    name = forms.CharField(max_length=50)