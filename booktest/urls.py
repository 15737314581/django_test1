# coding = utf-8
from django.urls import re_path
from booktest import views

urlpatterns = [
    re_path(r'^index$', views.index, name='index'),  # 建立/index与视图index之间的关系
    re_path(r'^books$', views.show_books),  # 显示图书信息
    re_path(r'^books/(\d+)$', views.detail),  # 显示图书关联的英雄信息
    re_path(r'^create$', views.create),  # 首页新增按钮
    re_path(r'^delete(\d+)$', views.delete),  # 删除点击的图书
    re_path(r'^areas$', views.areas),  # 广州市上下级信息
    re_path(r'^login$', views.login),  # 显示登录页面
    re_path(r'^login_check$', views.login_check),  # 校验登录
    re_path(r'^test_ajax$', views.test_ajax),  # 显示ajax页面
    re_path(r'^ajax_handle$', views.ajax_handle),  # ajax请求处理
    re_path(r'^login_ajax$', views.login_ajax),  # 显示ajax登录页面
    re_path(r'^login_ajax_check$', views.login_ajax_check),  # ajax登录请求处理
    re_path(r'^set_cookie$', views.set_cookie),  # 设置cookie
    re_path(r'^get_cookie$', views.get_cookie),  # 获取cookie
    re_path(r'^set_session$', views.set_session),  # 设置session
    re_path(r'^get_session$', views.get_session),  # 获取session
    re_path(r'^clear_session$', views.clear_session),  # 清除session
    re_path(r'^flush_session$', views.flush_session),  # 清除session
    re_path(r'^index1$', views.index1),  # 使用模版文件
    re_path(r'^change_pwd$', views.change_pwd),  # 显示修改密码页面
    re_path(r'^change_pwd_action$', views.change_pwd_action),  # 显示修改密码后的页面
    re_path(r'^verify_code$', views.verify_code),  # 生成验证码
    re_path(r'^url_reverse$', views.url_reverse),  # url反向解析页面
    re_path(r'^view_reverse$', views.view_reverse),  # 视图中的url反向解析
    re_path(r'^static_test$', views.static_test),  # 显示静态文件
    re_path(r'^show_upload$', views.show_upload),  # 显示上传文件页面
    re_path(r'^upload_action$', views.upload_action),  # 处理上传文件
    re_path(r'^show_area(?P<pindex>\d*)$', views.show_area),  # 显示省级城市
    re_path(r'^areas_detail$', views.areas_detail),  # 省市县选中案例
    re_path(r'^prov$', views.prov),  # 获取所有省级地区信息
    re_path(r'^city(\d+)$', views.city), # 获取省下面的市级信息
    re_path(r'^dis(\d+)$', views.city), # 获取省下面的市级信息

]
