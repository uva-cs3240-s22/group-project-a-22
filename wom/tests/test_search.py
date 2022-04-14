# https://docs.djangoproject.com/en/4.0/topics/testing/tools/
# https://docs.djangoproject.com/en/dev/ref/models/querysets/#in

from django.test import Client, TestCase
from wom.models import Recipe
from datetime import timedelta, timezone, datetime


def create_recipe(title, description, meal_type, course, cooking_time, preparation_time):
    """
    Create a recipe with the given parameters.
    """
    if not cooking_time:
        cooking_time = timedelta(days=50, seconds=27, microseconds=10,
                                milliseconds=29000, minutes=5, hours=8, weeks=2)
    if not preparation_time:
        preparation_time = timedelta(days=20, seconds=23, microseconds=13,
                                    milliseconds=29000, minutes=27, hours=3, weeks=2)
    return Recipe.objects.create(title=title, description=description, cooking_time=cooking_time, preparation_time=preparation_time, meal_type=meal_type, course=course)


class SearchTests(TestCase):
    def setUp(self):
        create_recipe(
            title="Demo recipe",
            description="this is a demo",
            meal_type="dinner",
            course="appetizer",
            preparation_time=timedelta(seconds=23, minutes=27, hours=3),
            cooking_time=timedelta(seconds=23, minutes=27, hours=0)
        ),
        create_recipe(
            title="Demo recipe no2",
            description="this is a demo2",
            meal_type="breakfast",
            course="side",
            preparation_time=timedelta(seconds=23, minutes=27),
            cooking_time=timedelta(seconds=3, minutes=20, hours=1)
        ),
        create_recipe(
            title="Peking Duck",
            description="this is a duck",
            meal_type="lunch",
            course="dessert",
            preparation_time=timedelta(seconds=23, minutes=27, hours=1),
            cooking_time=timedelta(seconds=53, minutes=47, hours=4)
        )

    def test_empty_search_input(self):
        """
        search function returns all recipes when a user clicks search after 
        inputting an empty string
        """
        response = self.client.get('/wom/search/?q=')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('title'), Recipe.objects.all().order_by('title'))

    def test_blank_space(self):
        """
        search function returns all recipes when a user clicks search after 
        inputting whitespace
        """

        response = self.client.get('/wom/search/?q=+++')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('title'), Recipe.objects.all().order_by('title'))

    def test_multiple_keywords(self):
        """
        search function returns items whose title contain all strings in
        the query when a user clicks search after inputting
        more than one keyword
        """

        response = self.client.get('/wom/search/?q=demo+rec+2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].first(
        ), Recipe.objects.get(title='Demo recipe no2'))

    def test_multiple_keywords_with_multiple_results(self):
        """
        search function returns items whose title contain all strings in
        the query when a user clicks search after inputting
        more than one keyword
        """

        response = self.client.get('/wom/search/?q=demo+rec')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['object_list'].order_by('title')), set(
            Recipe.objects.filter(title__in=['Demo recipe', 'Demo recipe no2']).order_by('title')))

class FilterTests(TestCase): 
    def setUp(self):
        create_recipe(
            title="Demo recipe",
            description="this is a demo",
            meal_type="dinner",
            course="appetizer",
            preparation_time=timedelta(seconds=23, minutes=27, hours=3),
            cooking_time=timedelta(seconds=23, minutes=27, hours=0)
        ),
        create_recipe(
            title="Demo recipe no2",
            description="this is a demo2",
            meal_type="breakfast",
            course="side",
            preparation_time=timedelta(seconds=23, minutes=27),
            cooking_time=timedelta(seconds=3, minutes=20, hours=1)
        ),
        create_recipe(
            title="Peking Duck",
            description="this is a duck",
            meal_type="lunch",
            course="dessert",
            preparation_time=timedelta(seconds=23, minutes=27, hours=1),
            cooking_time=timedelta(seconds=53, minutes=47, hours=4)
        )
    
    def test_filter_by_course(self):
        response = self.client.get('/wom/search/?course=appetizer')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('title'), Recipe.objects.all().filter(course__iexact="appetizer").order_by('title'))
    
    def test_filter_by_cook_time(self):
        response = self.client.get('/wom/search/?cook_time=1%3A00%3A00')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('title'), Recipe.objects.all().filter(cooking_time__lte=timedelta(hours=1)).order_by('title'))
    
    def test_filter_by_prep_time(self):
        response = self.client.get('/wom/search/?prep_time=1%3A00%3A00')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('title'), Recipe.objects.all().filter(preparation_time__lte=timedelta(hours=1)).order_by('title'))

    def test_filter_by_meal_type(self):
        response = self.client.get('/wom/search/?meal_type=dinner')
        self.assertEqual(response.status_code, 200)
        print('Filter by meal' , response.context['object_list'])
        self.assertQuerysetEqual(
        response.context['object_list'].order_by('title'), Recipe.objects.all().filter(meal_type__iexact="dinner").order_by('title'))
    
    def test_filter_many(self):
        response = self.client.get('/wom/search/?meal_type=breakfast&course=side&prep_time=00%3A30%3A00&cook_time=1%3A00%3A01')
        filters = {'meal_type__iexact': "breakfast", 'course__iexact': 'side', 'preparation_time__lte': timedelta(minutes=30), 'cooking_time__gte' : timedelta(hours=1)}
        print('Filter by many' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
        response.context['object_list'].order_by('title'), Recipe.objects.all().filter(**filters).order_by('title'))
    
    def test_filter_many_no_results(self):
        response = self.client.get('/wom/search/?meal_type=dinner&course=side&prep_time=00%3A30%3A00&cook_time=1%3A00%3A01')
        filters = {'meal_type__iexact': "dinner", 'course__iexact': 'side', 'preparation_time__lte': timedelta(minutes=30), 'cooking_time__gte' : timedelta(hours=1, seconds=1)}
        print('Filter by many no results' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
        response.context['object_list'].order_by('title'), Recipe.objects.all().filter(**filters).order_by('title'))
    
    def test_sort_by_hightest_rated_all_time(self):
        response = self.client.get('/wom/search/?sort_by=Highest')
        print('Filter by highest' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all().order_by('-avgRating'))
    
    def test_sort_by_hightest_rated_this_week(self):
        response = self.client.get('/wom/search/?sort_by=Highest_Week')
        print('Filter by week' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all().filter(pub_date__gte=(datetime.now(tz=timezone.utc)-timedelta(days=7))).order_by('-avgRating'))

    def test_sort_by_highest_rated_this_month(self):
        response = self.client.get('/wom/search/?sort_by=Highest_Month')
        print('Filter by month' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all().filter(pub_date__gte=(datetime.now(tz=timezone.utc)-timedelta(days=30))).order_by('-avgRating'))
    
    def test_sort_by_highest_rated_this_year(self):
        response = self.client.get('/wom/search/?sort_by=Highest_Month')
        print('Filter by year' , response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Recipe.objects.all().filter(pub_date__gte=(datetime.now(tz=timezone.utc)-timedelta(days=365))).order_by('-avgRating'))