from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    search_fields = [
        'user__username',
        'user__email'
        'author__username',
        'author__email',
    ]
    list_filter = ['user__username', 'author__username']
    empty_value_display = '-пусто-'

