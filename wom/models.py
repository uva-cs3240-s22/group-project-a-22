from django.db import models

# Create your models here.


class Recipe(models.Model):
    class MealTypes(models.TextChoices):
        BREAKFAST = 'breakfast'
        LUNCH = 'lunch'
        DINNER = 'dinner'
        DESSERT = 'dessert'
        OTHER = 'other'

    class Courses(models.TextChoices):
        APPETIZER = 'appetizer'
        ENTREE = 'entree'
        SIDE = 'side'
        SNACK = 'snack'
        OTHER = 'other'

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    cooking_time = models.DurationField()
    preparation_time = models.DurationField()
    meal_type = models.CharField(
        max_length=10, choices=MealTypes.choices, default=MealTypes.OTHER)
    course = models.CharField(
        max_length=10, choices=Courses.choices, default=Courses.OTHER)
    pub_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipes = models.ManyToManyField(Recipe)
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    units = models.CharField(max_length=5)

    def __str__(self):
        return self.name + " (" + str(self.quantity) + " " + self.units + ")"


class Instruction(models.Model):
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
