from django.contrib import admin, messages
from .models import Article, Rating, TextComment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','description','author','created_at','updated_at','rating']
    prepopulated_fields = {'slug' : ('title',)}

class ArticleRating(admin.ModelAdmin):
    list_display = ['amount','article','user']
    def save_model(self, request, obj, form, change):
        qs_exists = Rating.objects.filter(article = obj.article).filter(user = obj.user)
        if qs_exists:
            messages.error (request, 'User already provided a rating on this article')
            
        return super(ArticleRating, self).save_model(request, obj, form, change)

class TextCommentAdmin(admin.ModelAdmin):
    list_display = ['article','selected', 'author', 'body']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Rating, ArticleRating)
admin.site.register(TextComment, TextCommentAdmin)
