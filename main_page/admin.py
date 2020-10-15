from django.contrib import admin

from .models import User, Post


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password', 'salt')
    fields = ['id', 'username', 'email', 'password', 'salt']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'content', 'well_being', 'date', 'icon')
    fields = ['id', 'user_id', 'content', 'well_being', 'date', 'icon']
