from django.contrib import admin
from .models import Folder, Tag, Snippet


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color_accent', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'folder', 'is_favorite', 'is_public', 'created_at']
    list_filter = ['language', 'is_favorite', 'is_public', 'created_at', 'folder']
    search_fields = ['title', 'description', 'code', 'ai_summary', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
