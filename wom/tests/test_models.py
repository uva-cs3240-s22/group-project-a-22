from django.test import TestCase
from wom.models import Recipe, Instruction, Ingredient
from datetime import timedelta

from wom.views import search
# Create your tests here.

################################################
# Testing recipe, instruction, and ingredient models
################################################


def create_recipe(title, description):
    """
    Create a recipe with the given parameters.
    """
    cooking_time = timedelta(days=50, seconds=27, microseconds=10,
                             milliseconds=29000, minutes=5, hours=8, weeks=2)
    preparation_time = timedelta(days=20, seconds=23, microseconds=13,
                                 milliseconds=29000, minutes=27, hours=3, weeks=2)
    recipe = Recipe(title=title, description=description,
                    cooking_time=cooking_time, preparation_time=preparation_time)
    recipe.save()
    return recipe


def create_instruction(recipe, text):
    """
    Create an instruction with the given text.
    """

    instruction = Instruction(recipe=recipe, text=text)
    instruction.save()
    return instruction


def create_ingredient(recipe, name, quantity, units):
    """
    Create an ingredient with the given name, quantity, and units.
    """
    ingredient = Ingredient(recipe=recipe, name=name,
                            quantity=quantity, units=units)
    ingredient.save()
    return ingredient


class RecipeModelTests(TestCase):

    def test_recipe_was_created(self):
        """
        A recipe called 'chicken piccata' 
        is created with the appropriate title.
        """
        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        recipe = create_recipe(title, description)
        self.assertEquals(recipe.__str__(), "chicken piccata")


class InstructionModelTests(TestCase):

    def test_instruction_was_created__text(self):
        """
        An instruction step called 'wash lettuce'
        is created.
        """

        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        recipe = create_recipe(title, description)

        text = "wash lettuce"
        instruction = create_instruction(recipe, text)
        self.assertEquals(instruction.__str__(), "wash lettuce")

    def test_instruction_was_created__recipe(self):
        """
        An instruction step with recipe
        is created.
        """

        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        recipe = create_recipe(title, description)

        text = "wash lettuce"
        instruction = create_instruction(recipe, text)
        self.assertEquals(instruction.recipe.__str__(), "chicken piccata")


class IngredientModelTests(TestCase):

    def test_ingredient_was_created__properties(self):
        """
        An ingredient called "romaine lettuce"
        with quantity and units "1" and "lb" is 
        created.
        """
        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        recipe = create_recipe(title, description)

        name = "romaine lettuce"
        quantity = "1"
        units = "lb"
        ingredient = create_ingredient(recipe, name, quantity, units)
        self.assertEquals(ingredient.__str__(), "romaine lettuce (1 lb)")

    def test_ingredient_was_created__recipe(self):
        """
        An ingredient called "romaine lettuce"
        with quantity and units "1" and "lb" is 
        created.
        """
        title = "chicken piccata"
        description = "chicken in a lemon, butter, caper sauce"
        recipe = create_recipe(title, description)

        name = "romaine lettuce"
        quantity = "1"
        units = "lb"
        ingredient = create_ingredient(recipe, name, quantity, units)
        self.assertEquals(ingredient.recipe.__str__(), "chicken piccata")
