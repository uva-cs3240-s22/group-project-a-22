from csv import list_dialects
from django.contrib import admin

from wom.models import Ingredient, Recipe, FavoriteRecipe, Instruction, RateRecipe, Tag

# Register your models here.


class FavoriteInline(admin.StackedInline):
    model = FavoriteRecipe
    verbose_name = 'Favorited By User'
    verbose_name_plural = 'Favorites'
    extra = 3


class RateInline(admin.StackedInline):
    model = RateRecipe
    verbose_name = 'Rated By User'
    verbose_name_plural = 'Rating'
    extra = 3


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 3


class TagInline(admin.TabularInline):
    model = Tag
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'creator',
            'title',
            'description',
            'preparation_time',
            'cooking_time',
            'meal_type',
            'course',
            'anonymous_creator_bool',
            'avgRating',
            'numRatings'
        ]}),
        ('Fork Information', {'fields': ['parent'], 'classes': ['collapse']}),
        ('Date Information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [IngredientInline, InstructionInline, TagInline, RateInline]
    list_display = ['title', 'pub_date', 'meal_type']
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
