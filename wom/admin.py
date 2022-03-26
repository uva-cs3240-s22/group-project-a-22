from csv import list_dialects
from django.contrib import admin
from django.contrib.auth.models import User

from wom.models import Ingredient, Recipe, Instruction, FavoriteRecipe

# Register your models here.


class IngredientInline(admin.TabularInline):
    model = Ingredient


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 3


class FavoriteInline(admin.StackedInline):
    model = FavoriteRecipe
    verbose_name = 'Favorited By User'
    verbose_name_plural = 'Favorites'
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'title',
            'description',
            'preparation_time',
            'cooking_time',
            'meal_type',
            'course'
        ]}),
        ('Date Information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [IngredientInline, InstructionInline, FavoriteInline]

    list_display = ['title', 'pub_date', 'meal_type']
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
