from django.db import models
import uuid

# Create your models here.
class GoodsType(models.Model):
    """
    产品类型
    """
    gt_id = models.UUIDField(default=uuid.uuid1())
    gt_type = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.gt_type)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品类型"
        verbose_name_plural = "产品类型"

class GoodsColorType(models.Model):
    """
    产品颜色类型
    """
    gct_id = models.UUIDField(default=uuid.uuid1())
    gct_color_type = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    create_end_date = models.DateField(auto_now=True)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.gct_color_type)

    class Meta:
        ordering = ["pk"]
        verbose_name = "产品颜色类型"
        verbose_name_plural = "产品颜色类型"
