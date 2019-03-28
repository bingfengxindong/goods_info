from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    """
    用户表
    """
    u_id = models.UUIDField()
    u_login_name = models.CharField(max_length=100) #用户登录账号（六位数字）（自动生成的六位id：u123456）
    u_password = models.CharField(max_length=100) #用户密码（加密）
    u_username = models.CharField(max_length=100) #用户名
    u_phone_number = models.CharField(max_length=100) #手机号
    u_email = models.EmailField() #邮箱
    u_gen_time = models.DateField(auto_now_add=True) #创建时间
    u_reg_ip = models.CharField(max_length=100,default="0.0.0.0")  # 注册ip
    u_last_login_time = models.DateField(default=datetime(1900,1,1)) #最后登陆时间
    u_last_login_ip = models.CharField(max_length=100,default="0.0.0.0") #最后登录ip
    create_date = models.DateTimeField(default=datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.u_username)

    class Meta:
        ordering = ["pk"]
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

class UserLoginTime(models.Model):
    """
    用户历史登陆时间
    """
    ult_id = models.UUIDField()
    ult_login_time = models.DateField() #登陆时间
    ult_login_ip = models.CharField(max_length=100,default="0.0.0.0") #用户登录ip
    ult_user = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.ult_login_time)

    class Meta:
        ordering = ["pk"]
        verbose_name = "用户历史登陆时间"
        verbose_name_plural = "用户历史登陆时间"