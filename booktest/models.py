from django.db import models


# 设计和表对应的类，模型类
# Create your models here.
# 一类
class BookInfo(models.Model):
    """图书模型类"""
    # 图书名称
    btitle = models.CharField(max_length=20)
    # 出版时间
    bpub_date = models.DateField()


# 多类
class HeroInfo(models.Model):
    """英雄模型类"""
    # 英雄名称
    hname = models.CharField(max_length=20)
    # 英雄年龄
    hage = models.IntegerField()
    # 英雄性别
    hgender = models.BooleanField(default=False)
    # 备注
    hcomment = models.CharField(max_length=128)
    # 关系属性，和图书类是一对多关系
    hbook = models.ForeignKey('BookInfo',on_delete=models.CASCADE)
