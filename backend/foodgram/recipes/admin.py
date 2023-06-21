from django.contrib import admin

from .models import (
    Recipe, IngredientList, Favorite, Purchase, Subscription,
    Tag, Ingredient
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
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    list_editable = ('author',)
    search_fields = ('author__username', 'name',)
    list_filter = ('author', 'name',)
    empty_value_display = '-пусто-'


class IngredientListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredients',
        'amount',
    )
    list_editable = ('ingredients',)
    #search_fields = ('recipe__name', 'ingredients__product',)
    list_filter = ('recipe', 'ingredients',)
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


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'measurement_unit',
        # 'amount',
    )
    list_editable = ('product', 'measurement_unit',)
    # search_fields = ('text',)
    list_filter = ('product',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientList, IngredientListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
