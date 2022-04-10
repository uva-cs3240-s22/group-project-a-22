# Generated by Django 4.0.2 on 2022-04-03 21:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0027_alter_recipe_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='anonymous_creator_bool',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 3, 21, 58, 58, 619337, tzinfo=utc), verbose_name='Date Published'),
        ),
    ]
