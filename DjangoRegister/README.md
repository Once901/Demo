'''
时间：2020年5月20日
作者：志一
联系邮箱：Once09@163.com
'''

项目说明：
雏形，从登陆注册开始，主要以接口为主；

使用：
1。下载：
$pip install -r requirements.txt 
2。迁移同步：
$python manage.py makemigrations
$python manage.py migrate

3。运行：
python mannage.py runserver

4.注册中发送短信验证码接口个人的不能用，对于登陆接口测试，可以使用数据库的用户和密码登陆测试：
user：hello
password：123
phone：18310294727
icon：https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1694314525,975809133&fm=26&gp=0.jpg



**注意：
1。你对password做了makepassword之后，自己输入数据库的密码，在进行验证时时错误的，终端输入：
    $python manage.py shell
    >>> from django.contrib.auth.hashers import make_password
    >>> value = 123
    >>> res = make_password(value)
    >>> print(res)
    pbkdf2_sha256$150000$VDy0wT9NT4IC$pJtSRdPbF+EricN8WKmZWZpRcaLGdsOInH4cz6sBfj0=
    >>> exit()

