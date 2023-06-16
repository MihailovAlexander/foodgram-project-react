from django.contrib import admin

from .models import (
    Recipe, Favorite, Purchase, Subscription,
    Product, Tag, Recipe_tag, Ingredient
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'created',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class Recipe_tagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'tag',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'product',
        'measurement_unit',
    )
    # list_editable = ('group',)
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe_tag, Recipe_tagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
