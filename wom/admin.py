from csv import list_dialects
from django.contrib import admin

from wom.models import Ingredient, Recipe, FavoriteRecipe, Instruction

# Register your models here.


class FavoriteInline(admin.StackedInline):
    model = FavoriteRecipe
    verbose_name = 'Favorited By User'
    verbose_name_plural = 'Favorites'
    extra = 3

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3
# class IngredientQuantityInline(admin.TabularInline):
#     model = IngredientQuantity
#     extra = 3


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'title',
            'description',
            'preparation_time',
            'cooking_time',
            'meal_type',
            'course',
            'creator',
            'anonymous_creator_bool'
        ]}),
        ('Date Information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [IngredientInline, InstructionInline]
    # inlines = [IngredientQuantityInline, InstructionInline, FavoriteInline]
    list_display = ['title', 'pub_date', 'meal_type']
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
