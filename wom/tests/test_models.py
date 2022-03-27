from time import time
from django.forms import DurationField
from django.test import TestCase
from wom.models import Recipe, Instruction, Ingredient
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from http import HTTPStatus
# Create your tests here.

################################################
# Testing recipe, instruction, and ingredient models
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

class RecipeModelTests(TestCase):
    def test_dummy(self):
        self.assertEqual(1, 1)

    def test_recipe_was_created(self):
        """
        A recipe called 'chicken piccata' 
        is created with the appropriate title.
        """
        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        cooking_time = "5:00"
        preparation_time = "5:00"
        recipe = create_recipe(title, description)
        self.assertEquals(recipe.__str__(), "chicken piccata")

class InstructionModelTests(TestCase):

    def test_instruction_was_created(self):
        """
        An instruction step called 'wash lettuce'
        is created.
        """
        text = "wash lettuce"
        instruction = create_instruction(text)
        self.assertEquals(instruction.__str__(), "wash lettuce")

class IngredientModelTests(TestCase):

    def test_ingredient_was_created(self):
        """
        An ingredient called "romaine lettuce"
        with quantity and units "1" and "lb" is 
        created.
        """
        name = "romaine lettuce"
        quantity = "1"
        units = "lb"
        ingredient = create_ingredient(name, quantity, units)
        self.assertEquals(ingredient.__str__(), "romaine lettuce (1 lb)")