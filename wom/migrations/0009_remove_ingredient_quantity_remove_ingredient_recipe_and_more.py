# Generated by Django 4.0.2 on 2022-03-26 19:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0008_rename_favorites_recipe_favorite_favoriterecipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='units',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='favorite',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='course',
            field=models.CharField(choices=[('appetizer', 'Appetizer'), ('entree', 'Entree'), (
                'side', 'Side'), ('snack', 'Snack'), ('other', 'Other')], default='other', max_length=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='meal_type',
            field=models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), (
                'dinner', 'Dinner'), ('dessert', 'Dessert'), ('other', 'Other')], default='other', max_length=10),
        ),
        migrations.CreateModel(
            name='IngredientQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('units', models.CharField(blank=True, max_length=5)),
                ('ingredient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='wom.ingredient')),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='wom.recipe')),
            ],
        ),
    ]
