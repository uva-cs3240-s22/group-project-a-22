from time import time
from django.forms import DurationField
from django.http import HttpRequest
from django.test import TestCase
from wom.models import Recipe, Instruction, Ingredient, FavoriteRecipe
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from http import HTTPStatus
from django.contrib.auth.models import User


################################################
# Testing recipelist, createrecipe, search, and favorite views
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


class RecipeListViewTests(TestCase):
    def test_no_recipes(self):
        """
        If no recipes exist, an appropriate message is displayed.
        """

        response = self.client.get(reverse('wom:recipelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_created_recipe_is_shown(self):
        """
        Created recipes are shown on the recipe list
        """
        title = "caesar salad"
        description = "romaine lettuce with caesar dressing"
        recipe = create_recipe(title, description)
        response = self.client.get(reverse('wom:recipelist'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            [recipe],
        )


class CreateRecipeViewTests(TestCase):
    def test_create_page_loads(self):
        response = self.client.get(reverse('wom:createrecipe'))
        self.assertEqual(response.status_code, 200)

    # def test_form_success(self):
    #     recipe = create_recipe(
    #         "pepperoni pizza", "baked bread with cheese, tomato sauce, and pepperonis on top")
    #     crust = create_ingredient(recipe, "bread", "3", "lbs")
    #     step1 = create_instruction(recipe,
    #                                "prepare pizza dough and put cheese and pepperoni on")
    #     step2 = create_instruction(recipe, "bake for 20 minutes and eat")
    #     request = HttpRequest()
    #     request.POST = {
    #         "recipe": recipe,
    #     }


class SearchViewTests(TestCase):
    def test_empty_search_input(self):
        """
        search function ___ when a user clicks search after inputting
        an empty string or whitespace
        """
        response = self.client.get(reverse('wom:search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'], Recipe.objects.all())

    def test_link_to_detail_page(self):
        """
        search function ___ when a user clicks the title of a recipe on
        the search results page
        """

    def test_title(self):
        """
        search function returns 200 response and when a user clicks the title of a recipe on
        the search results page
        """

    def test_description(self):
        """
        search function returns queryset that contains all keywords within title
        """

    def test_empty_description(self):
        """
        search function returns queryset that begin with the character
        """


class FavoriteViewTests(TestCase):
    def test_backend_add_favorite(self):
        """
        add a recipe to favorites through the backend
        """
        testuser = User.objects.create_user(
            username='testuser', password='>JDI[kj>DAlJA*9a-')
        cooking_time = timedelta(
            days=50, seconds=27, microseconds=10, milliseconds=29000, minutes=5, hours=8, weeks=2)
        preparation_time = timedelta(
            days=20, seconds=23, microseconds=13, milliseconds=29000, minutes=27, hours=3, weeks=2)
        testrecipe = Recipe.objects.create(
            title='testrecipe', description='description', cooking_time=cooking_time, preparation_time=preparation_time)
        testfavorite = FavoriteRecipe.objects.create(
            user=testuser, recipe=testrecipe)
        self.assertQuerysetEqual(testuser.favorites.all(), [testfavorite])

    def test_backend_remove_favorite(self):
        """
        remove a recipe from favorites through the backend
        """
        testuser = User.objects.create_user(
            username='testuser', password='>JDI[kj>DAlJA*9a-')
        cooking_time = timedelta(
            days=50, seconds=27, microseconds=10, milliseconds=29000, minutes=5, hours=8, weeks=2)
        preparation_time = timedelta(
            days=20, seconds=23, microseconds=13, milliseconds=29000, minutes=27, hours=3, weeks=2)
        testrecipe = Recipe.objects.create(
            title='testrecipe', description='description', cooking_time=cooking_time, preparation_time=preparation_time)
        FavoriteRecipe.objects.create(user=testuser, recipe=testrecipe)
        testuser.favorites.filter(recipe=testrecipe).delete()
        self.assertQuerysetEqual(testuser.favorites.all(), [])
