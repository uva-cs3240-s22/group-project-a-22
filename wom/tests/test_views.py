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
from django.template import RequestContext
from django.template.loader import render_to_string


################################################
# Testing recipelist, createrecipe, search, favorite, and rating views
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

        response = self.client.get(reverse('wom:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes available")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_created_recipe_is_shown(self):
        """
        Created recipes are shown on the recipe list
        """
        title = "caesar salad"
        description = "romaine lettuce with caesar dressing"
        recipe = create_recipe(title, description)
        response = self.client.get(reverse('wom:search'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            [recipe],
        )


class CreateRecipeViewTests(TestCase):
    def test_create_page_no_login(self):
        response = self.client.get(reverse('wom:createrecipe'))\

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Log in with Google to create a new recipe.")

    def test_create_page_get(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)
        response = self.client.get(reverse('wom:createrecipe'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Create New Recipe")

    def test_create_page_post_failure(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        response = self.client.post(reverse('wom:createrecipe'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Create New Recipe")

    def test_create_page_post_success(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'recipe-anonymous_creator_bool': True,
            'instruction-TOTAL_FORMS': 1,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'ingredient-TOTAL_FORMS': 1,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipe = Recipe.objects.get(pk=1)

        self.assertEqual(recipe.title, 'Test Title')
        self.assertEqual(recipe.instruction_set.first().text,
                         'Test Instruction')
        self.assertEqual(recipe.ingredient_set.first().name, 'Test Ingredient')
        self.assertRedirects(response, reverse(
            'wom:detail', kwargs={"pk":1}), status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_create_page_post_no_instructions(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'ingredient-TOTAL_FORMS': 1,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
        }
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipes = Recipe.objects.all()

        self.assertEqual(list(recipes), [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Create New Recipe")

    def test_create_page_post_no_ingredients(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 1,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
        }
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipes = Recipe.objects.all()

        self.assertEqual(list(recipes), [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Create New Recipe")

    def test_create_page_post_multiple_instructions_and_ingredients(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipe = Recipe.objects.get(pk=1)
        instructions = list(recipe.instruction_set.all())
        ingredients = list(recipe.ingredient_set.all())

        self.assertEqual(recipe.title, 'Test Title')
        self.assertEqual(
            instructions[0].text, 'Test Instruction')
        self.assertEqual(
            instructions[1].text, 'Test Instruction 2')
        self.assertEqual(
            instructions[2].text, 'Test Instruction 3')
        self.assertEqual(
            ingredients[0].name, 'Test Ingredient')
        self.assertEqual(
            ingredients[1].name, 'Test Ingredient 2')
        self.assertEqual(
            ingredients[2].name, 'Test Ingredient 3')
        self.assertRedirects(response, reverse(
            'wom:detail', kwargs={"pk":1}), status_code=302, target_status_code=200, fetch_redirect_response=True)


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


class AccountViewTests(TestCase):
    def test_no_recipes_displayed_in_account(self):
        """
        If no recipes exist, an appropriate message is displayed
        for under 'My Account'.
        """
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)
        response = self.client.get(reverse('wom:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes available")
    
    def test_display_created_recipes(self):
        """
        'My Account' does not show recipes not created by 
        the logged in user
        """
        user = User.objects.get_or_create(username='testuser')[0]
        user1 = User.objects.get_or_create(username='testuser1')[0]

        self.client.force_login(user)
        form_data = {
            'recipe-title': 'Created by user',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        form_data1 = {
            'recipe-title': 'Not created by user',
            'recipe-creator': user1.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)
        self.client.force_login(user1)
        response1 = self.client.post(
            reverse('wom:createrecipe'), data=form_data1)
        self.client.force_login(user)

        recipes = Recipe.objects.all()

        response3 = self.client.get(reverse('wom:account'))
        self.assertEqual(response3.status_code, 200)
        self.assertContains(response3, "Created by user")
        self.assertNotContains(response3, "Not created by user")

class DeleteRecipeViewTests(TestCase):
    def test_recipe_is_deleted(self):    
        """
        When the user clicks delete, their the recipe is deleted
        """
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)
        form_data = {
            'recipe-title': 'Test',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipe = Recipe.objects.get(pk=1)
        response3 = self.client.get(reverse('wom:account'))

        self.assertContains(response3, "Test")

        response1 = self.client.get(reverse('wom:delete-recipe', args=(recipe.id,)))

        response3 = self.client.get(reverse('wom:account'))
        self.assertNotContains(response3, "Test")

class UpdateRecipeViewTests(TestCase):
    def test_update_template_loads(self):    
        """
        When the user clicks the edit button, the update template loads
        """
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)
        form_data = {
            'recipe-title': 'Test',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)

        recipe = Recipe.objects.get(pk=1)
        response3 = self.client.get(reverse('wom:account'))

        response1 = self.client.get(reverse('wom:update-recipe', args=(recipe.id,)))
        self.assertEqual(response1.status_code, 200)

    def test_recipes_updates(self):    
        """
        Recipes are successfully updated
        """
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)
        form_data = {
            'recipe-title': 'Test',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }
        
        response = self.client.post(
            reverse('wom:createrecipe'), data=form_data)
        
        form_data1 = {
            'recipe-title': 'Update',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
            'ingredient-TOTAL_FORMS': 3,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': 'oz',
            'ingredient-1-name': 'Test Ingredient 2',
            'ingredient-1-quantity': 2,
            'ingredient-1-units': 'lbs',
            'ingredient-2-name': 'Test Ingredient 3',
            'ingredient-2-quantity': 1,
            'ingredient-2-units': 'item',
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag',
        }

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.title, "Test")

        response = self.client.post(
        reverse('wom:update-recipe', args=(recipe.id,)), data=form_data1)
        recipe = Recipe.objects.get(pk=1)

        self.assertEqual(recipe.title, "Update")


class RatingViewTests(TestCase):
    def setUp(self):
        cooking_time = timedelta(
            days=50, seconds=27, microseconds=10, milliseconds=29000, minutes=5, hours=8, weeks=2)
        preparation_time = timedelta(
            days=20, seconds=23, microseconds=13, milliseconds=29000, minutes=27, hours=3, weeks=2)
        Recipe.objects.create(
            title='testrecipe', description='description', cooking_time=cooking_time,
            preparation_time=preparation_time)

    """
    Tests all major cases when rating a recipe
    Note that these are all combined into one test since many of the cases rely on previous cases having worked properly
    """
    def test_rating(self):
        """
        First Case: Test rating a recipe with no ratings.
        """

        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 0)
        self.assertEqual(recipe.numRatings, 0)

        self.client.post(reverse('wom:rate', args=[1, 5]), HTTP_REFERER='http://www.google.com')

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 5)
        self.assertEqual(recipe.numRatings, 1)

        """
        Second Case: Test rating a recipe that already has a rating from a different user.
        """

        user = User.objects.get_or_create(username='testuser2')[0]
        self.client.force_login(user)

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 5)
        self.assertEqual(recipe.numRatings, 1)

        self.client.post(reverse('wom:rate', args=[1, 2]), HTTP_REFERER='http://www.google.com')

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 3.5)
        self.assertEqual(recipe.numRatings, 2)

        """
        Third Case: Test changing the score given by a user who has already rated the recipe.
        """

        self.client.post(reverse('wom:rate', args=[1, 1]), HTTP_REFERER='http://www.google.com')

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 3)
        self.assertEqual(recipe.numRatings, 2)

        """Fourth Case: Test removing one user's rating from a recipe with multiple ratings"""

        self.client.post(reverse('wom:rate', args=[1, 6]), HTTP_REFERER='http://www.google.com')

        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 5)
        self.assertEqual(recipe.numRatings, 1)

        """Fifth/Final: Test removing a recipe's only rating"""
        user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(user)

        self.client.post(reverse('wom:rate', args=[1, 6]), HTTP_REFERER='http://www.google.com')
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.avgRating, 0)
        self.assertEqual(recipe.numRatings, 0)
