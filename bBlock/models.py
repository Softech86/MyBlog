from django.db import models
from django.contrib.auth.models import User

class bBlock(models.Model):
    name = models.CharField('版块名称', max_length = 30)
    desc = models.CharField('版块描述', max_length = 100)
    owner = models.ForeignKey(User, verbose_name = '管理员')
    
    create_timestamp = models.DateTimeField('创建时间', auto_now_add = True)
    last_update_timestamp = models.DateTimeField('修改时间', auto_now = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '版块'
        verbose_name_plural = '版块'
    