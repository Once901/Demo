'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
文件说明：关于app的一些路由
'''

from django.urls import path

from DJuser.views import UsersGenericAPIView

urlpatterns = [
    path('users/', UsersGenericAPIView.as_view()),
]