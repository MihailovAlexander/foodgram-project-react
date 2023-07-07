from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Favorite, Ingredient, IngredientList, Purchase, Recipe, Tag


admin.site.register(IngredientList)


class IngredientListInline(admin.TabularInline):
    model = IngredientList
    list_display = (
        'pk',
        'recipe',
        'ingredients',
        'amount',
    )
    list_editable = ('ingredients',)
    list_filter = ('recipe', 'ingredients',)
    empty_value_display = '-пусто-'


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
    inlines = [IngredientListInline, ]


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


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    resource_classes = [IngredientResource]


admin.site.register(Ingredient, IngredientAdmin)
