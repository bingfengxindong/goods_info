from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #产品类型
    url(r"^goods_type_upload",csrf_exempt(GoodsTypeUpload.as_view()),name="goods_type_upload"),
    url(r"^brand_goods_type_upload",csrf_exempt(BrandGoodsTypeUpload.as_view()),name="brand_goods_type_upload"), #品牌产品类型自动上传
    url(r"^brand_goods_type_classification",csrf_exempt(BrandGoodsTypeClassification.as_view()),name="brand_goods_type_classification"), #品牌产品类型自动分类
    url(r"^goods_type_list",csrf_exempt(GoodsTypeList.as_view()),name="goods_type_list"),
    url(r"^goods_type_top10",csrf_exempt(GoodsTypeHandler.as_view()),name="goods_type"),
    #产品颜色类型
    url(r"^goods_color_type_upload",csrf_exempt(GoodsColorTypeUpload.as_view()),name="goods_color_type_upload"),
    url(r"^brand_goods_color_type_upload",csrf_exempt(BrandGoodsColorTypeUpload.as_view()),name="brand_goods_color_type_upload"), #品牌产品颜色类型自动上传
    url(r"^brand_goods_color_type_classification",csrf_exempt(BrandGoodsColorTypeClassification.as_view()),name="brand_goods_color_type_classification"), #品牌产品颜色类型自动分类
    url(r"^goods_color_type_list",csrf_exempt(GoodsColorTypeList.as_view()),name="goods_color_type_list"),
    url(r"^goods_color_type_top10",csrf_exempt(GoodsColorTypeHandler.as_view()),name="goods_color_type"),
]