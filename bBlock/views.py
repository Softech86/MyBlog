from django.shortcuts import render
from django.template import RequestContext
from bBlock.models import bBlock

def index(request):
    blocks = bBlock.objects.all().order_by("id")
    return render(
        request,
        "index.html",
        {'blocks': blocks}, 
        context_instance = RequestContext(request)
    )