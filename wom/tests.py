import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from wom.views import search
from .models import Recipe, FavoriteRecipe


class SearchTests(TestCase):
    def test_empty_search_input(self):
        """
        search function ___ when a user clicks search after inputting
        an empty string or whitespace
        """
        response = self.client.get(reverse('wom:search')) #?
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes available")
        self.assertQuerysetEqual(response.context['posts'], [])

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


class FavoriteTests(TestCase):
    def test_backend_add_favorite(self):
        """
        add a recipe to favorites through the backend
        """
        testuser = User.objects.create_user(username='testuser', password='>JDI[kj>DAlJA*9a-')
        testrecipe = Recipe.objects.create(title='testrecipe')
        testfavorite = FavoriteRecipe.objects.create(user=testuser, recipe=testrecipe)
        self.assertQuerysetEqual(testuser.favorites.all(), [testfavorite])

    def test_backend_remove_favorite(self):
        """
        remove a recipe from favorites through the backend
        """
        testuser = User.objects.create_user(username='testuser', password='>JDI[kj>DAlJA*9a-')
        testrecipe = Recipe.objects.create(title='testrecipe')
        FavoriteRecipe.objects.create(user=testuser, recipe=testrecipe)
        testuser.favorites.filter(recipe=testrecipe).delete()
        self.assertQuerysetEqual(testuser.favorites.all(), [])


class DummyTestCase(TestCase):
    def test_dummy(self):
        self.assertEqual(1, 1)

