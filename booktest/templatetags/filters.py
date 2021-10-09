# coding = utf-8
# 自定义过滤器 过滤器的本质就是python函数
from django.template import Library

# 创建一个Library类的对象

library = Library()

@library.filter
# 自定义过滤器函数，至少有一个参数，最多2个参数
def mod(num):
    """自定义偶数过滤器 判断是否为偶数"""
    return num % 2 == 0
