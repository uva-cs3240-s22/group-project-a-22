# Generated by Django 4.0.2 on 2022-03-27 09:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0016_recipe_creator_alter_ingredient_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to='wom.recipe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.DurationField(),
        ),
    ]
