from django.contrib import admin

from wom.models import Ingredient, Recipe, Instruction

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)
