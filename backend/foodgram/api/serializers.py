from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientList, Purchase,
                            Recipe, Tag)
from users.models import Subscription, User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientListSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(
        source='ingredients.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredients.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientList
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]


class FullUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()

    def get_recipes(self, current_user):
        request = self.context.get('request')
        return RecipeDetailsSerializer(
            current_user.recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, current_user):
        return current_user.recipes.count()


class ShortUserSerializer(FullUserSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = ShortUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_ingredients(self, obj):
        ingredients = IngredientList.objects.filter(recipe=obj)
        return IngredientListSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Purchase.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class RecipeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = ('__all__', )


class SubscriptionSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        recipes = obj.author.recipes.all()
        serializer = RecipeDetailsSerializer(recipes, many=True)
        return serializer.data
