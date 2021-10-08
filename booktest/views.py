from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader, RequestContext
from booktest.models import BookInfo, AreaInfo
from datetime import date, datetime, timedelta


# Create your views here.
# 1：定义视图函数，HttpRequest
# 2: 进行url配置，建立URL与视图的对应关系
def my_render(request, template_path, context_dict={}):
    # 进行处理，和M和T进行交互
    # 使用模版文件
    # 1：加载模版文件，返回模版对象
    temp = loader.get_template(template_path)
    # 2: 定义模版上下文，给模版文件传递数据
    # context = RequestContext(request,{})
    # context = {}
    # 3：模版渲染，产生标准的html内容
    res_html = temp.render(context_dict, request=request)
    # 4：返回给浏览器
    return HttpResponse(res_html)


# def index(request):
#     return my_render(request,'booktest/index.html')

def index(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/index.html', {'books': books})


def create(request):
    b = BookInfo()
    b.btitle = '流星蝴蝶剑'
    b.bpub_date = date(2021, 9, 27)
    b.save()
    # 重定向到'/index'
    return HttpResponseRedirect('/index')
    # return redirect('/index') 重定向简写


def delete(request, bid):
    book = BookInfo.objects.get(id=bid)
    book.delete()
    return HttpResponseRedirect('/index')


def show_books(request):
    """显示图书信息"""
    # 1.通过M查找图书表中的数据
    books = BookInfo.objects.all()
    # 2.使用模版
    return render(request, 'booktest/show_books.html', {'books': books})


def detail(request, bid):
    """显示图书关联的英雄详情"""
    # 1.查找对应id的图书对象
    book = BookInfo.objects.get(id=bid)
    # 2.根据图书对象找到其关联的英雄列表
    heros = book.heroinfo_set.all()
    # 3.使用模版
    return render(request, 'booktest/detail.html', {'book': book, 'heros': heros})


def areas(request):
    """查询广州上下级城市"""
    # 查询广州信息
    area = AreaInfo.objects.get(atitle='广州市')
    # 查询广州上级信息
    parent = area.aParent
    # 查询广州下级信息
    childrens = area.areainfo_set.all()
    # 使用模版
    return render(request, 'booktest/areas.html', {'area': area, 'parent': parent, 'childrens': childrens})


def login(request):
    """显示登录页面"""
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        return redirect('/index')
    else:
        # 判断是否有cookie值username
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    """登录校验视图"""
    # 获取提交的用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # 校验登录内容
    if username == 'test' and password == '123456':
        # 登录成功，跳转首页
        response = redirect('/index')
        # 判断是否记住用户名
        if remember == 'on':
            response.set_cookie('username', username, max_age=60)
        # 设置表示已登录过的session
        request.session['islogin'] = True
        return response
    else:
        # 登录失败，跳转登录页
        return redirect('/login')


def test_ajax(request):
    """显示ajax页面"""
    return render(request, 'booktest/test_ajax.html')


def ajax_handle(request):
    """ajax请求处理"""
    # 返回json数据
    return JsonResponse({'res': 1})


def login_ajax(request):
    """显示ajax登录页面"""
    return render(request, 'booktest/login_ajax.html')


def login_ajax_check(request):
    """ajax登录请求处理"""
    # 获取请求用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 校验登录内容
    if username == 'test' and password == '123456':
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({"code": 0})


def set_cookie(request):
    """设置cookie"""
    response = HttpResponse('设置cookie')
    response.set_cookie('num', 1)
    # response.set_cookie('num', 1, max_age=14*24*3600)
    # response.set_cookie('num', 1, expires=datetime.now()+timedelta(days=14))
    return response


def get_cookie(request):
    """获取cookie"""
    num = request.COOKIES['num']
    return HttpResponse(num)


def set_session(request):
    """设置session"""
    request.session['username'] = 'abc'
    request.session['password'] = 123
    return HttpResponse('设置session')


def get_session(request):
    """获取session"""
    username = request.session['username']
    password = request.session['password']
    # 设置session过期时间单位为秒，0表示关联浏览器后失效
    # request.session.set_expiry(30)
    return HttpResponse(username+" : "+str(password))


def clear_session(request):
    """清除session——记录还在"""
    request.session.clear()
    return HttpResponse('清除session')


def flush_session(request):
    """清除session整条信息"""
    request.session.flush()
    return HttpResponse('清除session整条信息')