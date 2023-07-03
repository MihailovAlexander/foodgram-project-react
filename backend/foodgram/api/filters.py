from django_filters import rest_framework as filters
from recipes.models import Favorite, Purchase, Tag
from users.models import User


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    def get_is_favorited(self, queryset, filter_name, filter_value):
        favorites_ids = Favorite.objects.filter(
            user=self.request.user.pk
        ).values_list('recipe', flat=True)
        if filter_value:
            return queryset.filter(pk__in=favorites_ids)
        return queryset.exclude(pk__in=favorites_ids)

    def get_is_in_shopping_cart(self, queryset, filter_name, filter_value):
        purchase_ids = Purchase.objects.filter(
            user=self.request.user.pk
        ).values_list('recipe', flat=True)
        if filter_value:
            return queryset.filter(pk__in=purchase_ids)
        return queryset.exclude(pk__in=purchase_ids)