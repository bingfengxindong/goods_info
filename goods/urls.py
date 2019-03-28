from django.conf.urls import url
from .views import *
from .views_operate import *
from django.views.decorators.csrf import csrf_exempt

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
    url(r"^upload_data",csrf_exempt(GoodsUpload.as_view()),name="upload_data"), #产品信息上传
    url(r"^goods_match_color_upload",csrf_exempt(GoodsMatchColorUpload.as_view()),name="goods_match_color_upload"), #产品撞色信息上传
    url(r"^index",csrf_exempt(Index.as_view()),name="index"), #首页
    url(r"^goods_list",csrf_exempt(GoodsList.as_view()),name="goods_list"), #产品列表

    url(r"^goods_detail",csrf_exempt(GoodsDetailHandler.as_view()),name="goods_detail"), #产品详情
    url(r"^goods_image",csrf_exempt(GoodsImageHandler.as_view()),name="goods_image"), #产品图片

    url(r"^goods_collection",csrf_exempt(GoodsCollectionHandler.as_view()),name="goods_collection"), #产品收藏
    url(r"^goods_lable$",csrf_exempt(GoodsLableHandler.as_view()),name="goods_lable"), #产品标签
    url(r"^goods_lable_edit$",csrf_exempt(GoodsLableEditHandler.as_view()),name="goods_lable_edit"), #产品标签修改
    url(r"^goods_desc$",csrf_exempt(GoodsDescHandler.as_view()),name="goods_desc"), #产品描述
    url(r"^goods_desc_edit$",csrf_exempt(GoodsDescEditHandler.as_view()),name="goods_desc_edit"), #产品描述
    url(r"^goods_star",csrf_exempt(GoodsStarHandler.as_view()),name="goods_star"), #产品星级

    url(r"^goods_analysis_top10",csrf_exempt(GoodsAnalysisTop10.as_view()),name="goods_analysis_top10"), #产品位置变化top10

    url(r"^product_analysis",csrf_exempt(ProductAnalysis.as_view()),name="product_analysis"), #产品变化
    url(r"^goods_history",csrf_exempt(GoodsHistory.as_view()),name="goods_history"), #产品历史记录

    url(r"^user_center_info",csrf_exempt(UserCenterInfo.as_view()),name="user_center_info"), #用户个人中心
    url(r"^user_center_col",csrf_exempt(UserCenterCol.as_view()),name="user_center_col"), #用户个人中心
    url(r"^user_center_history",csrf_exempt(UserCenterHistory.as_view()),name="user_center_history"), #用户个人中心
]