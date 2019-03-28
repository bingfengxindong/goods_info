from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r"^change_data",csrf_exempt(GoodsChange.as_view()),name="change_data"),
]