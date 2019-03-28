from django.db import models
from goods.models import *
import uuid
import datetime

# Create your models here.

class ProductAnalysisConfirmation(models.Model):
    """
    产品分析确认
    """
    pac_id = models.UUIDField(default=uuid.uuid1())
    pac_brand = models.CharField(max_length=100) #品牌名字
    pac_type = models.CharField(max_length=50) #分析类型
    pac_before_time = models.DateField() #对比上次时间
    pac_now_time = models.DateField() #对比本次时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.pac_brand)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品分析确认"
        verbose_name_plural = "产品分析确认"

class GoodsPriceChange(models.Model):
    """
    产品价格变化
    """
    state = (
        (0,"不变"),
        (1,"上升"),
        (2,"下降"),
    )
    gpc_id = models.UUIDField(default=uuid.uuid1())
    gpc_price_type = models.CharField(max_length=10,default="$") #价格类型
    gpc_previous_price = models.CharField(max_length=20) #前一次价格
    gpc_now_price = models.CharField(max_length=20) #当前价格
    gpc_price_change = models.CharField(max_length=20) #价格变化
    gpc_price_state = models.IntegerField(choices=state,default=0) #价格变化状态
    gpc_previous_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="gpc_previous_goods") #前一次价格的商品
    gpc_now_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="gpc_now_goods") #当前价格的商品
    gpc_time = models.ForeignKey(Time,on_delete=models.CASCADE) #当前产品时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gpc_price_change)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品价格变化"
        verbose_name_plural = "产品价格变化"

class GoodsExtenceChange(models.Model):
    """
    产品上下架变化
    """
    state = (
        (0,"不变"),
        (1,"下架"),
        (2,"上架"),
    )
    gec_id = models.UUIDField(default=uuid.uuid1())
    gec_extence_type = models.IntegerField(choices=state,default=0) #上下架类型
    gec_extence_goods = models.ForeignKey(Goods,on_delete=models.CASCADE) #上下架产品
    gec_extence_now_time = models.DateField() #本期时间
    gec_extence_before_time = models.DateField()  #上期时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.gec_extence_goods.g_name)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品上下架变化"
        verbose_name_plural = verbose_name

class GoodsOrderChange(models.Model):
    """
    产品品牌网站位置
    """
    goc_id = models.UUIDField(default=uuid.uuid1())
    goc_previous_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="goc_previous_goods") #前一次产品
    goc_now_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="goc_now_goods") #当前产品
    goc_now_time = models.DateField()  # 本期产品时间
    goc_before_time = models.DateField()  # 上期产品时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.goc_now_goods.g_name)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品网站位置品牌"
        verbose_name_plural = "产品网站位置品牌"

class GoodsOrderChangeChange(models.Model):
    """
    产品网站位置变化
    """
    state = (
        (0,"不变"),
        (1,"上升"),
        (2,"下降"),
    )
    gocc_id = models.UUIDField(default=uuid.uuid1())
    gocc_now_goods_id = models.CharField(max_length=50) #当前产品详情的自定义id
    gocc_previous_order = models.IntegerField() #以前的位置
    gocc_now_order = models.IntegerField() #现在的位置
    gocc_order_change = models.CharField(max_length=20) #产品位置变化
    gocc_order_state = models.IntegerField(choices=state,default=0) #位置变化状态
    gocc_sex = models.CharField(max_length=20) #性别
    gocc_page = models.IntegerField(default=1) #产品页面编号
    goocc_goc = models.ForeignKey(GoodsOrderChange,on_delete=models.CASCADE) #产品网站位置品牌
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gocc_order_change)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品网站位置变化"
        verbose_name_plural = "产品网站位置变化"

class GoodsColorChange(models.Model):
    """
    产品颜色变化
    """
    state = (
        (0,"不变"),
        (1,"上升"),
        (2,"下降"),
    )
    gcc_id = models.UUIDField(default=uuid.uuid1())
    gcc_change_color_num = models.IntegerField() #产品颜色变化数量
    gcc_change_color_state = models.IntegerField(choices=state,default=0) #产品颜色变化类型
    gcc_previous_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="gcc_previous_goods") #前一次产品
    gcc_now_goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="now_goods") #当前产品
    gcc_time = models.DateField()  # 当前产品时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gcc_change_color_num)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品颜色变化"
        verbose_name_plural = "产品颜色变化"

class GoodsColorChangeColor(models.Model):
    """
    产品颜色变化的颜色
    """
    gccc_id = models.UUIDField(default=uuid.uuid1())
    gccc_color = models.CharField(max_length=100) #产品变化的颜色
    gccc_goodscolorchange = models.ForeignKey(GoodsColorChange,on_delete=models.CASCADE) #产品颜色变化
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gccc_color)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品颜色变化的颜色"
        verbose_name_plural = "产品颜色变化的颜色"
