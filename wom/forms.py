#######################
# REFERENCES:
# Title: StackOverflow Response to "Django formsets: make first required?"
# Author: mpen
# Date: February 9, 2011
# URL: https://stackoverflow.com/a/4951032
#######################

from mimetypes import init
from django import forms
from .models import Recipe, Instruction, Ingredient, Tag


class RecipeForm(forms.ModelForm):
    anonymous_creator_bool = forms.BooleanField(
        label="Make Creator Anonymous", required=False)
    image = forms.ImageField(label="Upload image of recipe")

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time',
                  'preparation_time', 'meal_type', 'course', 'anonymous_creator_bool', 'image']
        help_texts = {
            'cooking_time': 'Example format for a 1.5 hour cooking time: 1:30:00',
            'preparation_time': 'Example format for a 5 minute preparation time: 5:00',
        }


class RequiredFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True
        if (self.forms):
            self.forms[0].empty_permitted = False


class NotRequiredFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(NotRequiredFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True
