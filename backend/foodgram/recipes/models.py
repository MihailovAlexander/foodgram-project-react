from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('г', 'г'),
    ('кг', 'кг'),
    ('стакан', 'стакан'),
    ('по вкусу', 'по вкусу'),
    ('ст. л.', 'ст. л.'),
    ('шт.', 'шт.'),
    ('мл', 'мл'),
    ('ч. л.', 'ч. л.'),
    ('ст. л.', 'ст. л.'),
    ('капля', 'капля'),
    ('звездочка', 'звездочка'),
    ('щепотка', 'щепотка'),
    ('горсть', 'горсть'),
    ('кусок', 'кусок'),
    ('пакет', 'пакет'),
    ('долька', 'долька'),
    ('банка', 'банка'),
    ('упаковка', 'упаковка'),
    ('зубчик', 'зубчик'),
)
User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Кто подписывается',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='На кого подписывается',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    product = models.CharField(max_length=50)
    measurement_unit = models.CharField(
        max_length=16,
        choices=CHOICES
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self) -> str:
        return f'{self.product}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipes'
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='recipes.IngredientList',
        verbose_name='Ингредиенты блюда',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт владелец',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='recipe',
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество',
    )

    def __str__(self):
        return f'{self.recipe}, {self.ingredients}, {self.amount}'

    class Meta:
        ordering = ('recipe', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Список ингредиентов'

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
