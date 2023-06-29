from django.shortcuts import render
from recipes.models import Favorite  # RecipeIngredient,; ShoppingCart,
from recipes.models import Ingredient, IngredientList, Purchase, Recipe, Tag
from rest_framework import status, viewsets

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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


class RecipeViewSet(viewsets.ModelViewSet):
    """ Операции с рецептами: добавление/изменение/удаление/просмотр. """

    queryset = Recipe.objects.all()
    # permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    # pagination_class = CustomPagination
    # filter_backends = [DjangoFilterBackend, ]
    # filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        # return CreateRecipeSerializer
        return RecipeSerializer

    '''def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context'''