from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description')
    search_fields = ('title', 'description')
    empty_value_display = '-пусто-'
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
