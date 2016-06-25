from django.conf.urls import url
import register.views

urlpatterns = [
    url(r'^$', register.views.register_register, name = 'register_register'), 
]