# Generated by Django 3.2.12 on 2022-04-10 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wom', '0037_alter_recipe_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
    ]
