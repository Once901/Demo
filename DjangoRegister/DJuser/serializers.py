'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
'''

from rest_framework import serializers

from DJuser.models import DJUser


class DJUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = DJUser
        fields = ("id", "username", "phone", "icon")