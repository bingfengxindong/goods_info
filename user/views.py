from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.base import View
from goods.goods_query_view import *
from .u_id_generate import *
import uuid
import re
import datetime
# Create your views here.

def login_verify(func):
    def inner(self,request,*args,**kwargs):
        username = request.session.get("username")
        if not username:
            return redirect("/user/login")
        return func(self,request,*args,**kwargs)
    return inner

class Register(View):
    def get(self,request):
        context = {
            "title":"用户注册",
        }
        return render(request,"register.html",context=context)

    def post(self,request):
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        nickname = request.POST.get("nickname")
        pwd = request.POST.get("pwd")
        ip = query_ip(request)
        u_login_name = u_id()

        #一个邮箱或者手机号只能注册一个账号
        user_e = User.objects.filter(u_email=email)
        if len(user_e) == 1:
            return redirect("/user/register")
        user_p = User.objects.filter(u_phone_number=phone_number)
        if len(user_p) == 1:
            return redirect("/user/register")
        try:
            User.objects.create(
                u_id = uuid.uuid1(),
                u_login_name = u_login_name,
                u_password = pwd,
                u_username = nickname,
                u_phone_number = phone_number,
                u_email = email,
                u_reg_ip = ip,
            )
        except:
            return redirect("/user/register")
        return redirect("/user/login")

class Login(View):
    def get(self,request):
        context = {
            "title": "用户登录",
        }
        return render(request, "login.html", context=context)

    def post(self,request):
        account = request.POST.get("account")
        pwd = request.POST.get("pwd")
        if account[0] == "u":
            u_login_name = account
            user = User.objects.filter(u_login_name=u_login_name,u_password=pwd)
            if len(user) == 1:
                self.set_session(request,user[0])
                return redirect("/goods/index")
            else:
                return redirect("/user/login")
        elif re.match(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$",account):
            u_email = account
            user = User.objects.filter(u_email=u_email, u_password=pwd)
            if len(user) == 1:
                self.set_session(request, user[0])
                return redirect("/goods/index")
            else:
                return redirect("/user/login")
        else:
            u_phone_number = account
            user = User.objects.filter(u_phone_number=u_phone_number, u_password=pwd)
            if len(user) == 1:
                self.set_session(request, user[0])
                return redirect("/goods/index")
            else:
                return redirect("/user/login")

    def set_session(self,request,user):
        request.session["username"] = user.u_username
        request.session["u_login_name"] = user.u_login_name
        request.session.set_expiry(604800)
        ip = query_ip(request)
        user.u_last_login_time = datetime.datetime.now().date()
        user.u_last_login_ip = ip
        user.save()
        UserLoginTime.objects.create(
            ult_id = uuid.uuid1(),
            ult_login_time = datetime.datetime.now().date(),
            ult_login_ip = ip,
            ult_user = user,
        )

class KeepLogin(View):
    def get(self,request):
        username = request.session.get("username")
        return HttpResponse(username)

class Logout(View):
    def get(self,request):
        del request.session["username"]
        del request.session["u_login_name"]
        return redirect("/goods/index")