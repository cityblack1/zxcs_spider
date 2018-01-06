from django.db import models


class Novels(models.Model):
    title = models.CharField(max_length=24, verbose_name='标题')
    code = models.CharField(max_length=12, verbose_name='代码')
    size = models.FloatField(verbose_name='大小')
    abstract = models.TextField(verbose_name='摘要')
    category = models.CharField(max_length=56, verbose_name='分类')
    review = models.CharField(max_length=24, verbose_name='评价')
    created = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    class Meta:
        ordering = ('created', )
