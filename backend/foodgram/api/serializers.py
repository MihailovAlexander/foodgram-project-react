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


class AddIngredientListSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientList
        fields = ['id', 'amount']


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


class CreateRecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    ingredients = AddIngredientListSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def create_ingredients(self, ingrlist, recipe):
        for i in ingrlist:
            ingredient = Ingredient.objects.get(id=i['id'])
            IngredientList.objects.create(
                ingredients=ingredient, recipe=recipe, amount=i['amount']
            )

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):

        IngredientList.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        self.create_ingredients(ingredients, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context={
            'request': self.context.get('request')
        }).data
    

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
        request = self.context.get('user_request')
        recipes = obj.author.recipes.all()
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeDetailsSerializer(recipes, many=True)
        return serializer.data
