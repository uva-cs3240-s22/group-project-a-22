from django.test import Client, TestCase
from ..models import Recipe
from datetime import timedelta
def create_recipe(title, description):
    """
    Create a recipe with the given parameters.
    """
    cooking_time = timedelta( days=50, seconds=27, microseconds=10, 
        milliseconds=29000, minutes=5, hours=8, weeks=2)
    preparation_time = timedelta( days=20, seconds=23, microseconds=13, 
        milliseconds=29000, minutes=27, hours=3, weeks=2)
    return Recipe(title=title, description=description, cooking_time=cooking_time, preparation_time=preparation_time)

def setUp():
    create_recipe(
        title="Demo recipe",
        description="this is a demo",
    ),
    create_recipe(
        title="Demo recipe no2",
        description="this is a demo2",
    ),
    recipe = create_recipe(
        title="Peking Duck",
        description="this is a duck",
    )


class SearchTests(TestCase):
    
    def test_empty_search_input(self):
        """
        search function returns all recipes when a user clicks search after 
        inputting an empty string
        """
        setUp()
        c = Client()
        response = self.client.get('/wom/search/?q=')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all())

    def test_blank_space(self):
        """
        search function returns all recipes when a user clicks search after 
        inputting whitespace
        """

        response = self.client.get('/wom/search/?q=++')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all())

    
    # def test_multiple_keywords(self):
    #     """
    #     search function returns items whose title contain all strings in
    #     the query when a user clicks search after inputting
    #     more than one keyword
    #     """

    #     response = self.client.get('/wom/search/?q=demo+rec')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.get(id=1))


 


