from datetime import timedelta

from django.test import TestCase
from wom.models import *
from django.db import models


# Create your tests here.


# class DummyTestCase(TestCase):
#     def test_dummy(self):
#         self.assertEqual(1, 1)
#

class RecipeTestCase(TestCase):
    def setUp(self):
        testRecipe = Recipe(title="test", description="test", cooking_time=timedelta(),
                            preparation_time=timedelta(), meal_type="other", course="other")
        testRecipe.save()
        # print(testRecipe)

    def test_recipeCreated(self):
        self.assertEqual(True, Recipe.objects.get(title="test") in Recipe.objects.all())

    def test_fields(self):
        testRecipe = Recipe.objects.get(title="test")
        self.assertEqual(testRecipe.title, "test")
        self.assertEqual(testRecipe.description, "test")
        self.assertEqual(testRecipe.cooking_time, timedelta())
        self.assertEqual(testRecipe.preparation_time, timedelta())
        self.assertEqual(testRecipe.meal_type, "other")
        self.assertEqual(testRecipe.course, "other")

    def test_str(self):
        testRecipe = Recipe.objects.get(title="test")
        self.assertEqual(str(testRecipe), "test")


class IngredientTestCase(TestCase):

    def setUp(self):
        testRecipe = Recipe(title="test", description="test", cooking_time=timedelta(),
                            preparation_time=timedelta(), meal_type="other", course="other")
        testRecipe.save()
        testIngredient = Ingredient(recipe=testRecipe, name="testIngredient", quantity=1.0, units="cup")
        testIngredient.save()

    def test_ingredientCreated(self):
        testIngredient = Ingredient.objects.get(name="testIngredient")
        self.assertEqual(testIngredient.name, "testIngredient")
        self.assertEqual(testIngredient.quantity, 1.0)
        self.assertEqual(testIngredient.units, "cup")

    def test_recipeKey(self):
        testRecipe = Recipe.objects.get(title="test")
        testIngredient = Ingredient.objects.get(name="testIngredient")
        self.assertEqual(testIngredient.recipe, testRecipe)


class InstructionTestCase(TestCase):
    def setUp(self):
        testRecipe = Recipe(title="test", description="test", cooking_time=timedelta(),
                            preparation_time=timedelta(), meal_type="other", course="other")
        testRecipe.save()
        testInstruction = Instruction(text="testing instruction creation", recipe=testRecipe())
        testInstruction.save()

    def test_instructionCreation(self):
        testRecipe = Recipe.objects.get(title="test")
        testInstruction = Instruction.objects.get(text="testing instruction creation")
        self.assertEqual(testInstruction.text, "testing instruction creation")
        self.assertEqual(testInstruction.recipe, testRecipe)
