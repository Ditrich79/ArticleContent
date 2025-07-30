from django.contrib import admin
from .models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish', 'status']
    list_filter = ['status', 'created_at', 'publish', 'user']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['user']
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'email', 'is_active', 'created', 'updated']
    list_filter = ['is_active', 'created', 'updated']
    search_fields = ['name', 'email', 'content']
    ordering = ['-created', 'is_active']

