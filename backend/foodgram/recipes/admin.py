from django.contrib import admin

from .models import Favorite, Ingredient, IngredientList, Purchase, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'created',
    )
    fields = (
        ('name', 'author', 'cooking_time',),
        ('text', 'tags',),
        ('image',),
    )
    list_editable = ('author',)
    search_fields = ('author__username', 'name',)
    list_filter = ('author', 'name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientList)
class IngredientListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredients',
        'amount',
    )
    list_editable = ('ingredients',)
    list_filter = ('recipe', 'ingredients',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
