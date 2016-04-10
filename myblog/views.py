from django.shortcuts import render
from django.template import RequestContext

def home(request):
    return render(
        request,
        "home.html",
        context_instance = RequestContext(request)
    )
    
def notfound(request):
    return render(
        request,
        "notfound.html", 
        context_instance = RequestContext(request)
    )