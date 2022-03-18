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
    pub_date = models.DateTimeField('Date Published', default=timezone.now())

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    units = models.CharField(max_length=5)

    def __str__(self):
        return self.ingredient.name + " (" + str(self.quantity) + " " + self.units + ")"


class Instruction(models.Model):
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
