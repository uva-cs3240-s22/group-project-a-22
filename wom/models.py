# *******************************************
# REFERENCES:
# Title: Django Tutorial #27 - Foreign Keys
# Author: The Net Ninja
# Date: Jan 3, 2018
# URL: https://www.youtube.com/watch?v=zJWhizYFKP0
#
# * *************************************************
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    class MealTypes(models.TextChoices):
        OTHER = 'other'
        BREAKFAST = 'breakfast'
        LUNCH = 'lunch'
        DINNER = 'dinner'
        DESSERT = 'dessert'

    class Courses(models.TextChoices):
        OTHER = 'other'
        APPETIZER = 'appetizer'
        ENTREE = 'entree'
        SIDE = 'side'
        SNACK = 'snack'

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    preparation_time = models.DurationField()
    cooking_time = models.DurationField()
    meal_type = models.CharField(
        max_length=10, choices=MealTypes.choices, default=MealTypes.OTHER)
    course = models.CharField(
        max_length=10, choices=Courses.choices, default=Courses.OTHER)
    anonymous_creator_bool = models.BooleanField(default=False)
    pub_date = models.DateTimeField('Date Published', default=timezone.now)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name='children')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default='no-image.jpg')
    avgRating = models.FloatField(default=0)
    numRatings = models.IntegerField(default=0)


    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    units = models.CharField(max_length=10)

    def __str__(self):
        return self.name + " (" + str(self.quantity) + " " + self.units + ")"


class Instruction(models.Model):
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites')
    fav_date = models.DateTimeField('Date Favorited', default=timezone.now)


class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RateRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rating')
    score = models.FloatField()
    #comment = models.CharField(max_length=2000)
