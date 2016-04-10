from django.conf.urls import url
import novel.views

urlpatterns = [
    url(r'^list$', novel.views.novel_list, name = 'novel_list'), 
    url(r'^list/(?P<novel_id>\d+)$', novel.views.novel_index, name = 'novel_index'),
    url(r'^display/(?P<novel_id>\d+)/(?P<chapter_id>\d+)$', novel.views.novel_chapter_display, name = 'novel_chapter_display'),
]