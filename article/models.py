from django.db import models
from django.contrib.auth.models import User
from bBlock.models import bBlock

class Article(models.Model):
    title = models.CharField('标题', max_length = 30)
    text = models.CharField('正文', max_length = 1000)
    author = models.ForeignKey(User, verbose_name = '作者')
    block_obj = models.ForeignKey(bBlock, verbose_name = '版块')
    
    create_timestamp = models.DateTimeField('创建时间', auto_now_add = True)
    last_update_timestamp = models.DateTimeField('修改时间', auto_now = True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'