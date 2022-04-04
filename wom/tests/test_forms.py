from django.test import TestCase

from wom.forms import IngredientFormset, InstructionFormset, RecipeForm
from django.contrib.auth.models import User


class CreateRecipeFormTests(TestCase):
    def test_full_recipe_form(self):
        user = User.objects.get_or_create(username='testuser')[0]

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
        }
        form = RecipeForm(prefix='recipe', data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_recipe_form(self):
        form = RecipeForm(prefix='recipe', data={})

        self.assertFalse(form.is_valid())

    def test_incomplete_recipe_form(self):
        user = User.objects.get_or_create(username='testuser')[0]

        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': '',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
        }
        form = RecipeForm(prefix='recipe', data=form_data)

        self.assertFalse(form.is_valid())

    def test_full_instruction_form(self):
        form_data = {
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Test Instruction 1',
            'instruction-1-text': 'Test Instruction 2',
            'instruction-2-text': 'Test Instruction 3',
        }
        form = InstructionFormset(prefix='instruction', data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_instruction_form(self):
        form = InstructionFormset(prefix='instruction', data={})

        self.assertFalse(form.is_valid())

    def test_incomplete_instruction_form(self):
        form_data = {
            'instruction-TOTAL_FORMS': 1,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': '',
        }
        form = InstructionFormset(prefix='instruction', data=form_data)

        self.assertFalse(form.is_valid())

    def test_full_ingredient_form(self):
        form_data = {
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
        }
        form = IngredientFormset(prefix="ingredient", data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_ingredient_form(self):
        form = IngredientFormset(prefix="ingredient", data={})

        self.assertFalse(form.is_valid())

    def test_full_ingredient_form(self):
        form_data = {
            'ingredient-TOTAL_FORMS': 1,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-0-name': 'Test Ingredient',
            'ingredient-0-quantity': 3,
            'ingredient-0-units': '',
        }
        form = IngredientFormset(prefix="ingredient", data=form_data)

        self.assertFalse(form.is_valid())
