# Generated by Django 4.0.2 on 2022-03-27 10:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0023_alter_ingredient_recipe_alter_recipe_cooking_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
