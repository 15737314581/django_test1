from django.contrib import admin
from booktest.models import BookInfo, HeroInfo
from booktest.models import AreaInfo, PicTest


# 后台管理相关文件
# Register your models here.
# 自定义模型管理类
class BookInfoAdmin(admin.ModelAdmin):
    """图书模型管理类"""
    list_display = ['id', 'btitle', 'bpub_date', 'bread', 'bcomment', 'isDelete']


class HeroInfoAdmin(admin.ModelAdmin):
    """英雄人物模型管理类"""
    list_display = ['id', 'hname', 'hage', 'hgender', 'hcomment', 'hbook', 'isDelete']


class AreaStackedInline(admin.StackedInline):
    """以块状的方式嵌入"""
    # 写多类的名字
    model = AreaInfo
    # 可扩展的个数
    extra = 2


class AreaTabularInline(admin.TabularInline):
    """以表格的方式嵌入"""
    # 写多类的名字
    model = AreaInfo
    # 可扩展的个数
    extra = 2



class AreaInfoAdmin(admin.ModelAdmin):
    """地区模型管理类"""
    # 每页显示10条
    list_per_page = 10
    # 列表显示的内容
    list_display = ['id', 'atitle', 'title', 'parent']
    # actions_on_bottom = True
    # 页面右侧过滤栏
    list_filter = ['atitle']
    # 列表页上方的搜索框
    search_fields = ['atitle']
    # 编辑页面的展示字段顺序
    # fields = ['aParent','atitle']
    fieldsets = (
        ('基本', {'fields': ['atitle']}),
        ('高级', {'fields': ['aParent']})
    )
    # 将多类的块类名称放到一类中(块状的方式嵌入）
    # inlines = [AreaStackedInline]

    # 将多类的表格类名称放到一类中(表格的方式嵌入）
    inlines = [AreaTabularInline]


# 注册模型类
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(PicTest)
