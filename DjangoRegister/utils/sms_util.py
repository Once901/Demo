'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
文件说明：关于user中register的get验证码；
'''

import hashlib
import time
import uuid

import requests


def send_sms_code(phone):
    url = "https://api.netease.im/sms/sendcode.action"

    data = {
        "mobile": phone
    }

    app_key = "bd09b9119bc39b8fb448f80bbbcc1cc2"
    app_secret = "2ac0f2f3073b"

    nonce = uuid.uuid4().hex

    current_time = str(int(time.time()))
    # hashlib   python中内置摘要库   获取数据的摘要信息
    check_sum = hashlib.new("sha1", (app_secret + nonce + current_time).encode("utf-8")).hexdigest()

    headers = {
        "AppKey": app_key,
        "Nonce": nonce,
        "CurTime": current_time,
        "CheckSum": check_sum
    }

    response = requests.post(url, data=data, headers=headers)

    return response.json()


if __name__ == '__main__':
    result = send_sms_code("18842656895")
    print(result)