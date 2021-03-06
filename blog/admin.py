from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Comment, Category, Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
