import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Deepthoughts, Question


class SearchTests(TestCase):
    def test_empty_search_input(self):
        """
        search function ___ when a user clicks search after inputting
        an empty string or whitespace
        """
    
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

