from django.shortcuts import render
from django.template import RequestContext

# Create your views here.

def register_register(request):
    if request.method == 'GET':
        return render(
            request, 
            "register_register.html",
            context_instance = RequestContext(request)
        )