from unicodedata import category
from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
admin.site.register(Post)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
