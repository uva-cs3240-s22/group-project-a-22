# Generated by Django 4.0.2 on 2022-03-27 09:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0023_alter_ingredient_recipe_alter_recipe_cooking_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 9, 50, 1, 78791, tzinfo=utc), verbose_name='Date Published'),
        ),
    ]
