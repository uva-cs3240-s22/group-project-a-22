# Generated by Django 4.0.2 on 2022-03-30 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0027_merge_20220330_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to='wom.recipe'),
        ),
    ]
