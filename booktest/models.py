from django.db import models


# 设计和表对应的类，模型类
# Create your models here.
class BookInfoManager(models.Manager):
    """图书模型管理器类"""

    # 改变查询的结果集
    def all(self):
        # 调用父类的all方法，查询所有数据
        books = super().all()
        # 对数据进行过滤
        books = books.filter(isDelete=False)
        # 返回数据
        return books

    # 封装函数，操作模型类对应的数据表（增删改）
    def create_book(self, btitle, bpub_date):
        # 获取self所在的模型类
        model_class = self.model
        book = model_class()
        # book = BookInfo()
        book.btitle = btitle
        book.bpub_date = bpub_date
        book.save()
        return book

    def update_book(self, bid, new_btitle=None, new_bpub_date=None):
        model_class = self.model
        book = model_class.objects.get(id=bid)
        # book = BookInfo()
        if new_btitle is not None:
            book.btitle = new_btitle
        if new_bpub_date is not None:
            book.bpub_date = new_bpub_date
        book.save()
        return book

    def delete_book(self, bid):
        model_class = self.model
        book = model_class.objects.get(id=bid)
        # book = BookInfo()
        book.delete()


# 一类
class BookInfo(models.Model):
    """图书模型类"""
    # 图书名称
    btitle = models.CharField(max_length=20)
    # 出版时间
    bpub_date = models.DateField()
    # 阅读量
    bread = models.IntegerField(default=0)
    # 评论量
    bcomment = models.IntegerField(default=0)
    # 删除标记
    isDelete = models.BooleanField(default=False)
    # 自定义一个BookInfoManager类的对象
    objects = BookInfoManager()

    def __str__(self):
        # 返回书名
        return self.btitle


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
    hbook = models.ForeignKey('BookInfo', on_delete=models.CASCADE)
    # 删除标记
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        # 返回英雄名
        return self.hname


"""
class NewsType(models.Model):
    '''新闻类型类'''
    # 类型名
    type_name = models.CharField(max_length=20)
    # 关系属性 ，多对多
    type_news = models.ManyToManyField('NewsInfo')

    def __str__(self):
        # 返回类型名
        return self.type_name
    
    class Meta:
    # 指定模型类对应的表名
        db_table = 'newstype'


class NewsInfo(models.Model):
    '''新闻类'''
    # 新闻标题
    news_title = models.CharField(max_length=128)
    # 发布时间
    news_pub_date = models.DateTimeField(auto_now_add=True)
    # 新闻内容
    news_content = models.TextField()
    # 关系属性, 多对多
    # news_type = models.ManyToManyField('NewsType')

    def __str__(self):
        # 返回新闻标题
        return self.news_title
    
    class Meta:
    # 指定模型类对应的表名
        db_table = 'newsinfo'

class EmployeeBasicInfo(models.Model):
    '''员工基本信息表'''
    # 姓名
    name = models.CharField(max_length=20)
    # 性别
    gender = models.BooleanField(default=False)
    # 年龄
    age = models.IntegerField()
    # 关系属性 一对一
    employee_detail = models.OneToOneField('EmployeeDetailInfo')

    def __str__(self):
        # 返回员工姓名
        return self.name
    
    class Meta:
    # 指定模型类对应的表名
        db_table = 'employeebasicinfo'


class EmployeeDetailInfo(models.Model):
    '''员工详细信息表'''
    # 联系地址
    addr = models.CharField(max_length=128)
    # 联系电话
    phone = models.CharField(max_length=20)
    # 关系属性 一对一
    # employee_basic = models.OneToOneField(EmployeeBasicInfo)
    
    class Meta:
    # 指定模型类对应的表名
        db_table = 'employeedetailinfo'

"""


class AreaInfo(models.Model):
    """地区模型类"""
    # 地区名称
    atitle = models.CharField(max_length=20)
    # 关系属性，代表当前地区的上级地区
    aParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.atitle
