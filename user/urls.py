from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # 注册
    url(r"^register", csrf_exempt(Register.as_view()), name="register"),
    #登录
    url(r"^login",csrf_exempt(Login.as_view()),name="login"),
    url(r"^logout",csrf_exempt(Logout.as_view()),name="logout"),
    url(r"^keeplog",csrf_exempt(KeepLogin.as_view()),name="keeplog"),
]