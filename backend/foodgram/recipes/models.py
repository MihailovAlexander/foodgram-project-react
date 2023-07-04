from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    color = ColorField(max_length=7)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return f'{self.name}, {self.slug}'


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(
        max_length=16
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='recipes.IngredientList',
        verbose_name='Ингредиенты блюда',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ]

    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}, автор: {self.author}'


class IngredientList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт-владелец',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='recipe',
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        ordering = ('recipe__name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Список ингредиентов'

    def __str__(self):
        return f'{self.recipe}, {self.ingredients}, {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f'{self.user} / {self.recipe}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        related_name='purchases',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='purchases',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self) -> str:
        return f'{self.user} / {self.recipe}'
