from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

MAX_LENGTH_FIELD = 150


class User(AbstractUser):

    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH_FIELD,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_FIELD,
        blank=False
        )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_FIELD,
        blank=False
    )
    username = models.CharField(max_length=MAX_LENGTH_FIELD)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):

    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='authors',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='user_author_unique'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
