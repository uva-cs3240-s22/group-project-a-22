# Generated by Django 4.0.2 on 2022-03-27 09:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0017_alter_recipe_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 9, 35, 7, 746684, tzinfo=utc), verbose_name='Date Published'),
        ),
    ]
