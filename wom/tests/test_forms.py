from datetime import timedelta
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

from wom.forms import IngredientFormset, InstructionFormset, RecipeForm, TagFormset
from django.contrib.auth.models import User

from wom.models import Ingredient, Instruction, Recipe


class CreateRecipeFormTests(TestCase):
    def test_full_recipe_form(self):
        user = User.objects.get_or_create(username='testuser')[0]
        self.image_file = open(
            os.path.join(settings.BASE_DIR, 'wom/static/wom/images/test.jpg'), "rb"
        )
        form_data = {
            'recipe-title': 'Test Title',
            'recipe-creator': user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': 5,
            'recipe-preparation_time': 5,
            'recipe-meal_type': 'other',
            'recipe-course': 'other',
        }
        files_data = {
            'recipe-image': SimpleUploadedFile(
                self.image_file.name,
                self.image_file.read()
            )
        }

        form = RecipeForm(prefix='recipe', data=form_data, files=files_data)

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
    def test_full_tag_form(self):
        form_data = {
            'tag-TOTAL_FORMS': 3,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': 'Test Tag 1',
            'tag-1-name': 'Test Tag 2',
            'tag-2-name': 'Test Tag 3',
        }
        form = TagFormset(prefix='tag', data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_tag_form(self):
        form = TagFormset(prefix='tag', data={})

        self.assertFalse(form.is_valid())

    def test_incomplete_tagform(self):
        """
        Recipes should be able to have 0 tags
        """
        form_data = {
            'tag-TOTAL_FORMS': 1,
            'tag-INITIAL_FORMS': 0,
            'tag-0-name': '',
        }
        form = TagFormset(prefix='tag', data=form_data)

        self.assertTrue(form.is_valid())


class CreateRecipeForkTests(TestCase):
    def setUp(self):
        title = 'Example Recipe 1'
        description = 'This is an example recipe.'
        cooking_time = timedelta(minutes=30)
        preparation_time = timedelta(minutes=15)
        meal_type = 'breakfast'
        course = 'snack'
        recipe = Recipe(title=title, description=description, cooking_time=cooking_time,
                        preparation_time=preparation_time, meal_type=meal_type, course=course)
        recipe.save()

        instruction1 = Instruction(recipe=recipe, text='Instruction 1')
        instruction2 = Instruction(recipe=recipe, text='Instruction 2')
        instruction3 = Instruction(recipe=recipe, text='Instruction 3')
        instruction1.save()
        instruction2.save()
        instruction3.save()

        ingredient1 = Ingredient(
            recipe=recipe, name='Ingredient 1', quantity=5, units='oz')
        ingredient2 = Ingredient(
            recipe=recipe, name='Ingredient 2', quantity=10, units='lbs')
        ingredient3 = Ingredient(
            recipe=recipe, name='Ingredient 3', quantity=1, units='liter')
        ingredient1.save()
        ingredient2.save()
        ingredient3.save()

        self.user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(self.user)

    def test_fork_get(self):
        response = self.client.get(
            reverse('wom:createrecipe', kwargs={'recipe_id': 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Example Recipe 1")
        self.assertContains(response, "This is an example recipe.")
        self.assertContains(response, "00:30:00")
        self.assertContains(response, "00:15:00")
        self.assertContains(response, "breakfast")
        self.assertContains(response, "snack")

        self.assertContains(response, "Instruction 1")
        self.assertContains(response, "Instruction 2")
        self.assertContains(response, "Instruction 3")

        self.assertContains(response, "Ingredient 1")
        self.assertContains(response, "5.0")
        self.assertContains(response, "oz")
        self.assertContains(response, "Ingredient 2")
        self.assertContains(response, "10.0")
        self.assertContains(response, "lbs")
        self.assertContains(response, "Ingredient 3")
        self.assertContains(response, "1.0")
        self.assertContains(response, "liter")

    def test_fork_post(self):
        form_data = {
            'recipe-title': 'Example Recipe 1',
            'recipe-creator': self.user.pk,
            'recipe-description': 'Test description',
            'recipe-cooking_time': '00:30:00',
            'recipe-preparation_time': '00:15:00',
            'recipe-meal_type': 'lunch',
            'recipe-course': 'entree',
            'recipe-anonymous_creator_bool':True,
            'instruction-TOTAL_FORMS': 3,
            'instruction-INITIAL_FORMS': 0,
            'instruction-0-text': 'Instruction',
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
            reverse('wom:createrecipe', kwargs={'recipe_id': 1}), data=form_data)

        old_recipe = Recipe.objects.get(pk=1)
        old_instructions = list(old_recipe.instruction_set.all())
        old_ingredients = list(old_recipe.ingredient_set.all())

        new_recipe = Recipe.objects.get(pk=2)
        new_instructions = list(new_recipe.instruction_set.all())
        new_ingredients = list(new_recipe.ingredient_set.all())

        self.assertRedirects(response, reverse(
            'wom:detail', kwargs={"pk":2}), status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEqual(new_recipe.title, old_recipe.title)
        self.assertEqual(new_recipe.parent_id, old_recipe.pk)
        self.assertEqual(new_recipe.meal_type, 'lunch')
        self.assertEqual(old_recipe.meal_type, 'breakfast')

        self.assertEqual(
            new_instructions[0].text, 'Instruction')
        self.assertEqual(
            new_instructions[1].text, 'Test Instruction 2')
        self.assertEqual(
            new_instructions[2].text, 'Test Instruction 3')
        self.assertEqual(
            old_instructions[0].text, 'Instruction 1')
        self.assertEqual(
            old_instructions[1].text, 'Instruction 2')
        self.assertEqual(
            old_instructions[2].text, 'Instruction 3')

        self.assertEqual(
            new_ingredients[0].name, 'Test Ingredient')
        self.assertEqual(
            new_ingredients[1].name, 'Test Ingredient 2')
        self.assertEqual(
            new_ingredients[2].name, 'Test Ingredient 3')
        self.assertEqual(
            old_ingredients[0].name, 'Ingredient 1')
        self.assertEqual(
            old_ingredients[1].name, 'Ingredient 2')
        self.assertEqual(
            old_ingredients[2].name, 'Ingredient 3')
