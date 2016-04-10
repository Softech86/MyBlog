from django.conf.urls import url
import article.views

urlpatterns = [
    url(r'^lists/(?P<block_id>\d+)$', article.views.article_list, name = 'article_list'),
    url(r'^display/(?P<article_id>\d+)$', article.views.article_display, name = 'article_display'),
]
