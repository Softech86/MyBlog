from django.shortcuts import render
from django.template import RequestContext
from article.models import Article
from bBlock.models import bBlock

def article_list(request, block_id):
    articles = Article.objects.filter(block_obj = block_id).order_by("-id")
    block = bBlock.objects.get(id = block_id)
    return render(
        request,
        "article_list.html",
        {'block_obj': block, 'articles': articles}, 
        context_instance = RequestContext(request)
    )
    
def article_display(request, article_id):
    article = Article.objects.get(id = article_id)
    block = bBlock.objects.get(id = article.block_obj.id)
    return render(
        request,
        "article_display.html",
        {'block_obj': block, 'article': article},
        context_instance = RequestContext(request)
    )