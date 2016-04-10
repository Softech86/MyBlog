from django.contrib import admin
from novel.models import Novel, Chapter 

class NovelAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'desc', 'yisou_id', 'resource', 'latest_chapter', 'latest_chapter_id', 'create_timestamp', 'last_update_timestamp', )
    list_filter = ('author', )
    
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('novel', 'title', 'chapter_id', 'chapter_order', 'create_timestamp', 'last_update_timestamp', )
    list_filter = ('novel', )
    
admin.site.register(Novel, NovelAdmin)
admin.site.register(Chapter, ChapterAdmin)