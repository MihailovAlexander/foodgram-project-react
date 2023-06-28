from django.shortcuts import render
from recipes.models import Favorite  # RecipeIngredient,; ShoppingCart,
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status, viewsets

from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    #permission_classes = [AllowAny, ]
    pagination_class = None
    # filter_backends = [IngredientFilter, ]
    #search_fields = ['^name', ]
