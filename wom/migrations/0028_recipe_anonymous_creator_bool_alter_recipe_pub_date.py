# Generated by Django 4.0.2 on 2022-04-03 21:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0027_merge_20220330_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='anonymous_creator_bool',
            field=models.BooleanField(default=False),
        ),
    ]
