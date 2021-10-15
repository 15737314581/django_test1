# coding = utf-8
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BlockedIPSMiddleware(MiddlewareMixin):
    """中间件类"""
    EXCLUDE_IPS = []

    # 中间件函数，在视图函数调用前被调用
    def process_view(self, request, view_func, *args, **kwargs):
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Forbidden</h1>')


class TestMiddleware(MiddlewareMixin):
    """中间件类"""

    def __init__(self,get_response=None):
        # 服务器重启后，接受第一个请求时调用
        super().__init__()
        self.get_response =get_response
        print('----init-----')

    def process_request(self, request):
        # 产生request对象之后，匹配url之前调用
        print('----process_request------')

    def process_view(self, request, view_func, *args, **kwargs):
        # 匹配url之后，视图函数调用之前调用
        print('----process_view------')

    def process_response(self, request, response):
        # 视图函数调用之后，内容返回浏览器之前
        print('----process_response------')
        return response

    def process_exception(self,request,exception):
        # 视图发生异常时调用
        print('----process_exception------')
        print(exception)


