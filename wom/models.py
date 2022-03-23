from django.db import models
from django.utils import timezone

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
    cooking_time = models.DurationField()
    preparation_time = models.DurationField()
    meal_type = models.CharField(
        max_length=10, choices=MealTypes.choices, default=MealTypes.OTHER)
    course = models.CharField(
        max_length=10, choices=Courses.choices, default=Courses.OTHER)
    pub_date = models.DateTimeField('Date Published', default=timezone.now)
    creator = models.CharField(max_length=100, default="Anonymous")

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.FloatField(default=0)
    units = models.CharField(max_length=5)

    def __str__(self):
        return self.name + " (" + str(self.quantity) + " " + self.units + ")"


class Instruction(models.Model):
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
