# Generated by Django 4.0.2 on 2022-04-07 19:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0033_recipe_avgscore_alter_favoriterecipe_fav_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='numRatings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='favoriterecipe',
            name='fav_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 19, 56, 53, 501959, tzinfo=utc), verbose_name='Date Favorited'),
        ),
    ]
