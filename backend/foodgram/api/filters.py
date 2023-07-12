from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Tag
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
        if filter_value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, filter_name, filter_value):
        if filter_value:
            return queryset.filter(purchases__user=self.request.user)
        return queryset


class IngredientNameFilter(SearchFilter):
    search_param = 'name'
