# Generated by Django 4.0.2 on 2022-04-03 22:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0028_recipe_anonymous_creator_bool_alter_recipe_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 3, 22, 5, 47, 185412, tzinfo=utc), verbose_name='Date Published'),
        ),
    ]
