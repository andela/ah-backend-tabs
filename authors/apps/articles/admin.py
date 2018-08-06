from django.contrib import admin
from .models import Article, ArticleImage

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 3

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','description','created_at','updated_at', ]
    inlines = [ArticleImageInline, ]
    prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Article, ArticleAdmin)
