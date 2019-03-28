from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(BrandType)
admin.site.register(Brand)
admin.site.register(BrandTime)
admin.site.register(Time)
admin.site.register(Goods)
admin.site.register(GoodsInformation)
admin.site.register(GoodsSize)
admin.site.register(GoodsDetail)
admin.site.register(GoodsImage)
admin.site.register(GoodsComment)
admin.site.register(BrandGoodsType)
admin.site.register(BrandGoodsColorType)

admin.site.register(GoodsStar)
admin.site.register(GoodsCollection)
admin.site.register(BrowseHistory)
admin.site.register(GoodsLable)
admin.site.register(GoodsCustomDescription)
