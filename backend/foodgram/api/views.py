from datetime import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientList, Purchase,
                            Recipe, Tag)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscription, User

from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FullUserSerializer, IngredientSerializer,
                          RecipeDetailsSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        recipe_obj = get_object_or_404(Recipe, pk=pk)
        args_user_recipe = {
            'user': request.user,
            'recipe': recipe_obj,
        }
        if request.method == 'POST':
            return create_record(
                obj=recipe_obj,
                obj_class=Favorite,
                request_args=args_user_recipe,
                serializer=RecipeDetailsSerializer
            )
        elif request.method == 'DELETE':
            return delete_record(
                obj_class=Favorite,
                request_args=args_user_recipe
            )

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        recipe_obj = get_object_or_404(Recipe, pk=pk)
        args_user_recipe = {
            'user': request.user,
            'recipe': recipe_obj,
        }
        if request.method == 'POST':
            return create_record(
                obj=recipe_obj,
                obj_class=Purchase,
                request_args=args_user_recipe,
                serializer=RecipeDetailsSerializer
            )
        elif request.method == 'DELETE':
            return delete_record(
                obj_class=Purchase,
                request_args=args_user_recipe
            )

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        if not request.user.purchases.exists():
            return Response(
                {'errors': 'Ваш список покупок пуст!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shopping_recipes = Recipe.objects.filter(
            pk__in=[
                Purchase.objects.filter(
                    user=self.request.user
                ).values_list('recipe', flat=True)
            ]
        ).values_list('pk', flat=True)
        total_ingredients = IngredientList.objects.filter(
            recipe__in=shopping_recipes,
        ).values(
            'ingredients__name',
            'ingredients__measurement_unit',
        ).annotate(
            Sum('amount', distinct=True)
        )
        today = datetime.now().strftime("%Y.%m.%d")
        txt_list = []
        txt_list.append(f'"Продуктовый помощник". Покупки на {today}:')
        for ingredient in total_ingredients:
            txt_list.append(
                (
                    f'* {ingredient.get("ingredients__name")} '
                    f'({ingredient.get("ingredients__measurement_unit")})'
                    + f' - {ingredient.get("amount__sum")}'
                )
            )
        response = HttpResponse(
            content='\n'.join(txt_list),
            content_type='text/plain; charset=UTF-8',
        )
        response['Content-Disposition'] = (
            f'attachment; filename=Shopping_List({today}).txt'
        )
        return response


class SubscribeView(APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        author_obj = get_object_or_404(User, pk=id)
        if request.user == author_obj:
            return Response(
                {'errors': 'Нельзя подписываться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            'user': request.user,
            'author': author_obj
        }

        already_existed, created = Subscription.objects.get_or_create(**data)
        if not created:
            return Response(
                {'errors': 'Ошибка при создании записи.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            FullUserSerializer(
                author_obj,
                context={'user_request': request.user}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if not Subscription.objects.filter(
           user=request.user, author=author).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        subscription = get_object_or_404(
            Subscription, user=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(ListAPIView):

    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = request.user.followers.all()
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'user_request': request.user}
        )
        return self.get_paginated_response(serializer.data)


def create_record(obj, obj_class, request_args, serializer):
    already_existed, created = obj_class.objects.get_or_create(**request_args)
    if not created:
        return Response(
            {'errors': 'Ошибка при создании записи.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        serializer(obj).data,
        status=status.HTTP_201_CREATED,
    )


def delete_record(obj_class, request_args):
    try:
        record = obj_class.objects.get(**request_args)
    except obj_class.DoesNotExist:
        return Response(
            {'errors': 'Удаление не удалось.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    record.delete()
    return Response(
        {'detail': 'Удаление успешно.'},
        status=status.HTTP_204_NO_CONTENT,
    )
