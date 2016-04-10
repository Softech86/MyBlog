from django.conf.urls import url
import bBlock.views

urlpatterns = [
    url(r'^index$', bBlock.views.index, name = 'block_index'), 
]