from django.contrib import admin

from wom.models import Ingredient, Recipe, Instruction

# Register your models here.


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3


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
            'favorites'
        ]}),
        ('Date Information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [IngredientInline, InstructionInline]
    list_display = ['title', 'pub_date', 'meal_type']
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Recipe, RecipeAdmin)
