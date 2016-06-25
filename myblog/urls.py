from django.conf.urls import url, include
from django.contrib import admin
import myblog.views

urlpatterns = [
    url(r'^admin/?$', admin.site.urls),
    url(r'^$', myblog.views.home, name = 'home'),
    url(r'^block/', include('bBlock.urls')),
    url(r'^article/', include('article.urls')),
    url(r'^novel/', include('novel.urls')),
    url(r'^register', include('register.urls')),
    url(r'', myblog.views.notfound, name = 'notfound')
]
