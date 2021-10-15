from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader, RequestContext
from booktest.models import BookInfo, AreaInfo, PicTest
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
# import six
# from six.moves.urllib.request import urlopen
# from six.moves.urllib.parse import urljoin
# from django.utils.six import BytesIO
from six import BytesIO

# Create your views here.
# 1：定义视图函数，HttpRequest
# 2: 进行url配置，建立URL与视图的对应关系
from django_test1 import settings


def login_required(view_func):
    """登录判断装饰器"""

    def wrapper(request, *args, **kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录，调用对应的视图
            return view_func(request, *args, **kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/login')

    return wrapper


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


def my_render1(request, template_path, context={}):
    """自定义模版"""
    # 加载模版文件，获取一个模版对象
    temp = loader.get_template(template_path)
    # 定义模版上下文，给模版文件传递数据
    context = RequestContext(request, context)
    # 模版渲染，产生一个替换的html内容
    res_html = temp.render(context)
    # 返回应答
    return HttpResponse(res_html)


def index1(request):
    """使用模版文件"""
    return my_render1(request, 'booktest/index1.html')


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
    # 获取用户输入的验证码
    vcode1 = request.POST.get('vcode')
    # 获取保存在session中的验证码
    vcode2 = request.session.get('verifycode')
    # 进行验证码校验
    if vcode1.lower() != vcode2.lower():
        msg = '验证码有误，请重新输入～'
        request.session['msg'] = msg
        return redirect('/login')
    # 校验登录内容
    if username == 'test' and password == '123456':
        # 登录成功，跳转首页
        response = redirect('/index')
        # 判断是否记住用户名
        if remember == 'on':
            response.set_cookie('username', username, max_age=60)
        # 设置表示已登录过的session
        request.session['islogin'] = True
        request.session['username'] = username
        return response
    else:
        # 登录失败，跳转登录页
        msg = '用户名或密码错误，请重新输入～'
        request.session['msg'] = msg
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
    return HttpResponse(username + " : " + str(password))


def clear_session(request):
    """清除session——记录还在"""
    request.session.clear()
    return HttpResponse('清除session')


def flush_session(request):
    """清除session整条信息"""
    request.session.flush()
    return HttpResponse('清除session整条信息')


@login_required
def change_pwd(request):
    """显示修改密码页面"""
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    """显示修复密码完成后的页面"""
    password = request.POST.get('pwd')
    username = request.session.get('username')
    return HttpResponse('{0}的新密码为：{1}'.format(username, password))


def verify_code(request):
    """验证码函数"""
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'images/png')


def url_reverse(request):
    """url反向解析页面"""
    return render(request, 'booktest/url_reverse.html')


from django.urls import reverse


def view_reverse(request):
    """视图中的反向解析"""
    # 重定向到/index
    url = reverse('booktest:index')
    return redirect(url)


def static_test(request):
    """展示静态文件"""
    print('视图函数被调用')
    return render(request, 'booktest/static_test.html')


def show_upload(request):
    """展示上传图片页面"""
    return render(request, 'booktest/upload_pic.html')


def upload_action(request):
    """上传图片处理"""
    # 获取上传文件的处理对象
    pic = request.FILES['pic']
    pic_path = '{0}/booktest/{1}'.format(settings.MEDIA_ROOT, pic.name)

    # 创建文件
    with open(pic_path, 'wb') as f:
        # 获取上传文件的内容并写入到创建的文件中
        for content in pic.chunks():
            f.write(content)

    # 在数据库中保存上传记录
    PicTest.objects.create(goods_pic='booktest/{}'.format(pic.name))

    # 返回
    return HttpResponse('ok')


from django.core.paginator import Paginator


def show_area(request, pindex):
    """分页显示省级信息"""
    # 查询出所有省级地区信息
    areas = AreaInfo.objects.filter(aParent__isnull=True)
    # 分页
    paginator = Paginator(areas, 10)
    print(paginator.num_pages)
    print(paginator.page_range)
    if pindex == '':
        # 默认展示第一页内容
        pindex = 1
    else:
        pindex = int(pindex)
    # 获取第pindex页的内容
    page = paginator.page(pindex)
    return render(request, 'booktest/show_area.html', {'areas': areas, 'page': page})


def areas_detail(request):
    """省市县选中案例"""
    return render(request, 'booktest/areas_detail.html')


def prov(request):
    """获取所有省级地区的信息"""
    areas = AreaInfo.objects.filter(aParent__isnull=True)
    # 遍历areas 返回一个json对象
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))

    return JsonResponse({'data': areas_list})


def city(request,pid):
    """获取省下面的市级信息"""
    # 获取id对应的省份对象
    # area = AreaInfo.objects.get(id=pid)
    # 获取该省份下面的所有市级信息
    # areas = area.areainfo_set.all()
    areas = AreaInfo.objects.filter(aParent=pid)
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))

    return JsonResponse({'data': areas_list})
