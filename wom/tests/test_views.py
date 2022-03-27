from time import time
from django.forms import DurationField
from django.http import HttpRequest
from django.test import TestCase
from wom.models import Recipe, Instruction, Ingredient
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from http import HTTPStatus

################################################
# Testing recipelist and createrecipe views
################################################

def create_recipe(title, description):
    """
    Create a recipe with the given parameters.
    """
    cooking_time = timedelta( days=50, seconds=27, microseconds=10, 
        milliseconds=29000, minutes=5, hours=8, weeks=2)
    preparation_time = timedelta( days=20, seconds=23, microseconds=13, 
        milliseconds=29000, minutes=27, hours=3, weeks=2)
    return Recipe(title=title, description=description, cooking_time=cooking_time, preparation_time=preparation_time)

def create_instruction(text):
    """
    Create an instruction with the given text.
    """
    return Instruction(text=text)

def create_ingredient(name, quantity, units):
    """
    Create an ingredient with the given name, quantity, and units.
    """
    return Ingredient(name=name, quantity=quantity, units=units)

class RecipeListViewTests(TestCase):
    def test_created_recipe_is_shown(self):
        """
        Created recipes are shown on the recipe list
        """
        title = "caesar salad"
        description = "romaine lettuce with caesar dressing"
        recipe = create_recipe(title, description)
        recipe.save()
        response = self.client.get(reverse('wom:recipelist'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            [recipe],
        )

    def test_no_recipes(self):
        """
        If no recipes exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('wom:recipelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes are available.")
        self.assertQuerysetEqual(response.context['object_list'], [])

class CreateRecipeViewTests(TestCase):
    def test_create_page_loads(self):
        response = self.client.get(reverse('wom:recipelist'))
        self.assertEqual(response.status_code, 200)

    # def test_form_success(self):
    #     recipe = create_recipe("pepperoni pizza", "baked bread with cheese, tomato sauce, and pepperonis on top")
    #     crust = create_ingredient("bread", "3", "lbs")
    #     step1 = create_instruction("prepare pizza dough and put cheese and pepperoni on")
    #     step2 = create_instruction("bake for 20 minutes and eat")
    #     request = HttpRequest()
    #     request.POST = {
    #         "recipe": recipe,

    #     }

