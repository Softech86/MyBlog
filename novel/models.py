from django.db import models

class Novel(models.Model):
    name = models.CharField('书名', max_length = 30)
    author = models.CharField('作者', max_length = 30)
    desc = models.CharField('简介', max_length = 3000)
    yisou_id = models.PositiveIntegerField('宜搜ID')
    latest_chapter = models.CharField('最新章节', max_length = 30)
    latest_chapter_id = models.CharField('最新章节ID', max_length = 30)
    last_update_timestamp = models.DateTimeField('更新时间', auto_now = False)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add = True)
    resource = models.CharField('来源网站', max_length = 30)
    
    def __str__(self):
        return self.name
       
    class Meta:
        verbose_name = '小说'
        verbose_name_plural = '小说'
     

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, verbose_name = '书名')
    chapter_id = models.IntegerField('章节编号')
    chapter_order = models.CharField('章节序号', max_length = 30)
    title = models.CharField('章节名', max_length = 30)
    content = models.TextField('正文')
    create_timestamp = models.DateTimeField('创建时间', auto_now_add = True)
    last_update_timestamp = models.DateTimeField('更新时间', auto_now = True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节'
