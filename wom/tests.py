import datetime

from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse

from wom.views import search
from .models import Recipe
from django.db import models
from django.utils import timezone


class SearchTests(TestCase):
    # def setUp(self):
    #     # self.client = Client()
    #     # self.search_url = reverse('wom:search', args=['1']) #how to add query there?
    #     Recipe.objects.create(
    #         title="Demo recipe",
    #         description="this is a demo",
    #         preparation_time=1,
    #         cooking_time=1,
    #         meal_type="lunch",
    #         course="snack",
    #         pub_date= "March 24, 2022, 10:01 p.m."
    #     )
    def test_empty_search_input(self):
        """
        search function returns all recipes when a user clicks search after 
        inputting an empty string
        """
        c = Client()
        response = c.get('/wom/search/?q=')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post'], Recipe.objects.all())

    def test_blank_space(self):
        """
        search function ___ when a user clicks search after inputting
        whitespace
        """
        c = Client()
        response = c.get('/wom/search/?q=++')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post'], Recipe.objects.all())
        print(Recipe.objects.all())
    
    def test_multiple_keywords(self):
        """
        search function returns items whose title contain all strings in
        the query when a user clicks search after inputting
        more than one keyword
        """
        c = Client()
        response = c.get('/wom/search/?q=bb+chick')
        self.assertEqual(response.status_code, 200)
        # self.assertQuerysetEqual(response.context['post'], Recipe.objects.get())

    def test_post_data(self):
        """
        search function returns 200 response and when a user clicks the title of a recipe on
        the search results page
        """
        c = Client()
        response = c.get('/wom/1')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post'], Recipe.objects.get())
        self.assertEqual(response.context['post']['title'], "")
        self.assertEqual(response.context['post']['description'], "")
        self.assertEqual(response.context['post']['ingredients'], "")

 


