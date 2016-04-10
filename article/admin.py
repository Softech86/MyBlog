from django.contrib import admin
from article.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'block_obj', 'create_timestamp', 'last_update_timestamp')
    list_filter = ('author', )
    
admin.site.register(Article, ArticleAdmin)