'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
文件说明：关于user用户的模型
'''
from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class DJUser(models.Model):
    username = models.CharField(max_length=32, unique=True, null=False)
    _password = models.CharField(max_length=256)
    phone = models.CharField(max_length=16, unique=True, null=False)
    icon = models.CharField(max_length=256, null=True, default="")

    class Meta:
        db_table="DJ_user"

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,value):
        self._password = make_password

    def verify_password(self,value):
        return check_password(value,self._password)



