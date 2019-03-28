from django.db import models
from tinymce.models import HTMLField
import django.utils.timezone as timezone
from goods_type.models import *
from user.models import *
import uuid
import datetime
# Create your models here.

class BrandType(models.Model):
    """
    品牌类型
    """
    bt_id = models.UUIDField(default=uuid.uuid1())
    bt_type = models.CharField(max_length=100) #品牌类型
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.bt_type)

    class Meta:
        ordering = ["pk"]
        verbose_name = "品牌类型"
        verbose_name_plural = "品牌类型"

class Brand(models.Model):
    """
    品牌
    """
    b_id = models.UUIDField(default=uuid.uuid1())
    b_name = models.CharField(max_length=100) #品牌名字
    b_url = models.CharField(max_length=100,default="") #品牌网址
    b_logo = models.ImageField(upload_to="image",default="image/brand_logo/logo.png") #品牌logo
    b_bt = models.ForeignKey(BrandType,on_delete=models.CASCADE) #品牌类型
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.b_name)

    class Meta:
        ordering = ["pk"]
        verbose_name = "品牌"
        verbose_name_plural = "品牌"

class BrandTime(models.Model):
    """
    品牌抓取时间、根据品牌的目录、确认品牌是否上传、抓取的数据以时间为目录
    """
    bt_id = models.UUIDField(default=uuid.uuid1())
    bt_time = models.DateField() #品牌抓取时间
    bt_brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return "%s-%s"%(str(self.bt_time),self.bt_brand.b_name)

    class Meta:
        ordering = ["pk"]
        verbose_name = "品牌抓取时间"
        verbose_name_plural = "品牌抓取时间"

class Time(models.Model):
    """
    数据时间
    """
    t_id = models.UUIDField(default=uuid.uuid1())
    t_time = models.DateField() #产品数据时间
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.t_time)

    class Meta:
        ordering = ["pk"]
        verbose_name = "数据时间"
        verbose_name_plural = "数据时间"

class Goods(models.Model):
    """
    产品
    """
    g_id = models.UUIDField(default=uuid.uuid1())
    g_name = models.CharField(max_length=100) #产品名字
    g_title = models.CharField(max_length=100,default="")  # 产品标题
    g_price_type = models.CharField(max_length=20,default="$") #产品价格种类
    g_discount_price = models.CharField(max_length=20, default="0")  # 产品上期价格
    g_now_price = models.CharField(max_length=20) #产品本期价格
    g_time = models.ForeignKey(Time, on_delete=models.CASCADE) #产品时间
    b_brand = models.ForeignKey(Brand,on_delete=models.CASCADE) #产品所属品牌
    g_type = models.ForeignKey(GoodsType,on_delete=models.CASCADE) #产品类型
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return "%s-%s"%(str(self.g_name),self.b_brand.b_name)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品"
        verbose_name_plural = "产品"

class GoodsInformation(models.Model):
    """
    产品信息
    """
    gi_id = models.UUIDField(default=uuid.uuid1())
    gi_model = models.CharField(max_length=100,default=0) #产品网站型号（含拼接）
    gi_color = models.CharField(max_length=100) #产品颜色
    gi_match_color = models.BooleanField(default=False) #是否撞色
    gi_order = models.IntegerField() #产品位置
    gi_gender = models.CharField(max_length=50) #产品使用人群
    gi_brand_goods_url = models.TextField(null=True,blank=True) #产品抓取网页url
    gi_page = models.IntegerField() #产品网页编号
    gi_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    gi_color_type = models.ForeignKey(GoodsColorType,on_delete=models.CASCADE) #产品颜色类型
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gi_model)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品信息"
        verbose_name_plural = "产品信息"

class GoodsSize(models.Model):
    """
    产品尺寸
    """
    gs_id = models.UUIDField(default=uuid.uuid1())
    gs_size = models.CharField(max_length=20) #产品尺寸
    gs_gi = models.ForeignKey(GoodsInformation,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gs_size)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品尺寸"
        verbose_name_plural = "产品尺寸"

class GoodsDetail(models.Model):
    """
    产品详情
    """
    gd_id = models.UUIDField(default=uuid.uuid1())
    gd_detail = models.CharField(max_length=1000) #产品详情
    gd_gi = models.ForeignKey(GoodsInformation,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gd_detail)

    class Meta:
        ordering = ["pk"]
        verbose_name = "详情"
        verbose_name_plural = "详情"

class GoodsImage(models.Model):
    """
    产品图片
    """
    gimg_id = models.UUIDField(default=uuid.uuid1())
    gimg_path = models.CharField(max_length=100) #图片
    gimg_url = models.CharField(max_length=200) #图片url
    gimg_gi_goods = models.ForeignKey(GoodsInformation,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gimg_path)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品图片"
        verbose_name_plural = "产品图片"

class GoodsComment(models.Model):
    """
    产品评论
    """
    gc_id = models.UUIDField(default=uuid.uuid1())
    gc_comment_time = models.DateField() #评论时间
    gc_comment = models.CharField(max_length=800) #评论
    gc_comment_star = models.IntegerField() #评论星级
    gc_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gc_comment)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品评论"
        verbose_name_plural = "产品评论"


#产品分类目录
class BrandGoodsType(models.Model):
    """
    品牌产品类型
    """
    bgt_id = models.UUIDField(default=uuid.uuid1())
    bgt_goods_name = models.CharField(max_length=100)
    bgt_goods_type = models.CharField(max_length=50)
    bgt_brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return "%s-%s"%(self.bgt_goods_name,self.bgt_goods_type)

    class Meta:
        ordering = ["pk"]
        verbose_name = "品牌产品类型"
        verbose_name_plural = "品牌产品类型"

class BrandGoodsColorType(models.Model):
    """


    品牌产品颜色类型
    """
    bgct_id = models.UUIDField(default=uuid.uuid1())
    bgct_goods_color = models.CharField(max_length=100)
    bgct_goods_color_type = models.CharField(max_length=50)
    bgct_brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return "%s-%s" % (self.bgct_goods_color, self.bgct_goods_color_type)

    class Meta:
        ordering = ["pk"]
        verbose_name = "品牌产品颜色类型"
        verbose_name_plural = "品牌产品颜色类型"

#功能

class GoodsStar(models.Model):
    """
    产品星级
    """
    gs_id = models.UUIDField(default=uuid.uuid1())
    gs_star = models.IntegerField(default=0) #产品星级
    gs_goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    gs_user = models.ForeignKey(User,null=True,blank=True,default=None,on_delete=models.CASCADE)
    gs_create_date = models.DateTimeField(default=datetime.datetime.now)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gs_star)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品星级"
        verbose_name_plural = "产品星级"

class GoodsCollection(models.Model):
    """
    产品收藏
    """
    collection = (
        (0,"未收藏"),
        (1,"已收藏"),
    )
    gc_id = models.UUIDField(default=uuid.uuid1())
    gc_collection = models.IntegerField(choices=collection,default=0) #产品收藏
    gc_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    gc_user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    gc_create_date = models.DateTimeField(default=datetime.datetime.now)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gc_collection)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品收藏"
        verbose_name_plural = "产品收藏"

class BrowseHistory(models.Model):
    """
    产品浏览历史
    """
    bh_id = models.UUIDField(default=uuid.uuid1())
    bh_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    bh_user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    bh_create_date = models.DateTimeField(default=datetime.datetime.now)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return "%s---%s"%(self.bh_goods,self.create_date)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品浏览历史"
        verbose_name_plural = "产品浏览历史"

class GoodsLable(models.Model):
    """
    产品标签
    """
    gl_id = models.UUIDField(default=uuid.uuid1())
    gl_lable = models.CharField(max_length=100) #产品标签
    gl_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    gl_user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    gl_create_date = models.DateTimeField(default=datetime.datetime.now)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gl_lable)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品标签"
        verbose_name_plural = "产品标签"

class GoodsCustomDescription(models.Model):
    """
    产品自定义描述
    """
    gcd_id = models.UUIDField(default=uuid.uuid1())
    gcd_description = HTMLField() #产品自定义描述
    gcd_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    gcd_user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    gcd_create_date = models.DateTimeField(default=datetime.datetime.now)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gcd_description)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品自定义描述"
        verbose_name_plural = "产品自定义描述"