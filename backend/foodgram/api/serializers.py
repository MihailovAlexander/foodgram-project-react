from djoser.serializers import UserCreateSerializer, UserSerializer
# from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Tag
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'product', 'measurement_unit']