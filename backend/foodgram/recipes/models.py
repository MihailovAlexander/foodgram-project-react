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


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='recipes')
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Кто подписывается',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        verbose_name='На кого подписывается',
        on_delete=models.CASCADE,
    )

class Product(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)


class Recipe_tag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
    )
    measurement_unit = models.CharField(
        max_length=16,
        choices=CHOICES
    )
