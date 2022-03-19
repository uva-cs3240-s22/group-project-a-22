# Generated by Django 4.0.2 on 2022-03-19 04:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0002_remove_ingredient_quantity_remove_ingredient_recipes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='course',
            field=models.CharField(choices=[('other', 'Other'), ('appetizer', 'Appetizer'), ('entree', 'Entree'), ('side', 'Side'), ('snack', 'Snack')], default='other', max_length=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='meal_type',
            field=models.CharField(choices=[('other', 'Other'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('dessert', 'Dessert')], default='other', max_length=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 4, 39, 24, 872536, tzinfo=utc), verbose_name='Date Published'),
        ),
    ]
