'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
'''

import secrets
import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from DJuser.models import DJUser
from DJuser.serializers import DJUserSerializer
from utils.sms_util import send_sms_code


class UsersGenericAPIView(GenericAPIView):

    def post(self, request):
        action = request.data.get("action")

        if action == "check_username":
            return self.do_check_username(request)
        elif action == "check_phone":
            return self.do_check_phone(request)
        elif action == "get_phone_code":
            return self.do_get_phone_code(request)
        elif action == "register":
            return self.do_register(request)
        elif action == "login":
            return self.do_login(request)
        elif action == "userinfo":
            return self.get_user_info(request)
        else:
            raise ValidationError(detail="请提供正确的动作")

    def do_check_username(self, request):
        username = request.data.get("username")

        # 可以在此添加各种数据校验规则

        if username and not DJUser.objects.filter(username=username).exists():

            data = {
                "msg": "用户名可用",
                "status": status.HTTP_200_OK
            }
        else:
            data = {
                "msg": "用户名不可用",
                "status": status.HTTP_400_BAD_REQUEST
            }

        return Response(data)

    def do_check_phone(self, request):
        phone = request.data.get("phone")

        # 可以在此添加各种数据校验规则

        if phone and not DJUser.objects.filter(phone=phone).exists():

            data = {
                "msg": "手机号可用",
                "status": status.HTTP_200_OK
            }
        else:
            data = {
                "msg": "手机号不可用",
                "status": status.HTTP_400_BAD_REQUEST
            }

        return Response(data)

    def do_get_phone_code(self, request):
        phone = request.data.get("phone")

        # 可以在此添加各种数据校验规则
        """
            1. 调用短信发送平台API
            2. 存储短信验证码的值
            3. 包装Response进行返回
        """

        result = send_sms_code(phone)#自己的用完了，暂时不能发送成功了，如有试验者，可自定写这

        print(result)

        if result["code"] == 200:
            verify_code = str(result["obj"])
            # 存储验证码，  验证码要和手机号有关联， 之后还需要获取验证
            cache.set("register_verify_code" + phone, verify_code, timeout=300)

            data = {
                "msg": "验证码发送成功",
                "status": status.HTTP_200_OK
            }

            return Response(data)

        data = {
            "msg": "验证码发送失败",
            "status": status.HTTP_400_BAD_REQUEST
        }

        return Response(data)

    def do_register(self, request):

        phone = request.data.get("phone")
        username = request.data.get("username")
        password = request.data.get("password")
        verify_code = request.data.get("verify_code")

        cache_verify_code = cache.get("register_verify_code" + phone)

        if verify_code != cache_verify_code:

            data = {
                "msg": "验证码错误",
                "status": status.HTTP_400_BAD_REQUEST
            }

            return Response(data)

        user = DJUser()
        user.phone = phone
        user.username = username
        user.password = password
        try:
            user.save()
        except Exception as e:
            print(e)
            data = {
                "msg": "验证错误："+ str(e),
                "status": status.HTTP_400_BAD_REQUEST
            }

            return Response(data)

        data = {
            "msg": "注册成功",
            "status": status.HTTP_201_CREATED,
            # 将对象转换成字典
            "data": DJUserSerializer(user).data
        }

        return Response(data)

    def do_login(self, request):

        login_type = request.data.get("login_type")

        if login_type == "usernamepassword":
            return self.do_login_usernamepassword(request)
        else:
            raise ValidationError(detail="请选择正确的登陆方式")

    def do_login_usernamepassword(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        users = DJUser.objects.filter(username=username)

        if not users.exists():
            raise NotFound(detail="用户不存在")
        user = users.first()

        if not user.verify_password(password):
            raise ValidationError(detail="密码错误")

        # token = uuid.uuid4().hex
        # python3.6 新增内置模块，可以直接生成token
        token = secrets.token_hex()

        # 存储token
        cache.set(token, user.id, timeout=60*60*24*7)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "登陆成功",
            "data": {
                "token": token
            }
        }

        return Response(data)

    def get_user_info(self, request):
        try:
            token = request.data.get("token")

            user_id = cache.get(token)

            user = DJUser.objects.get(pk=user_id)
        except Exception as e:
            print(e)
            raise NotFound(detail="用户状态失效")

        data = {
            "msg": "获取成功",
            "status": status.HTTP_200_OK,
            "data": DJUserSerializer(user).data
        }

        return Response(data)