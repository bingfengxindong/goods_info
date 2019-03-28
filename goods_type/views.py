from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.base import View
from django.core.paginator import Paginator
from goods.goods_query_view import *
from django.db.models import Q
from goods_info.settings import BASE_DIR
from goods.update_goods_data import *
from .models import *
import uuid
import json
import os
import datetime

class GoodsTypeUpload(View):
    """
    产品类型上传
    """
    def get(self,request):
        b_name = request.GET.get("b_name","")
        t_time = request.GET.get("t_time","")
        brands = Brand.objects.filter().order_by("pk")
        if b_name == "":
            brand = brands[0]
        else:
            brand = Brand.objects.get(b_name=b_name)
        times = Time.objects.filter().order_by("pk")
        if t_time == "":
            time_t = times[0]
        else:
            time_t = Time.objects.get(t_id=t_time)
        goodss = Goods.objects.filter(g_time=time_t,b_brand=brand)
        goods_data = []
        for goods in goodss:
            gi = GoodsInformation.objects.filter(gi_goods=goods)[0]
            gimg = GoodsImage.objects.filter(gimg_gi_goods=gi)[0]
            gdetails = [i.gd_detail for i in GoodsDetail.objects.filter(gd_gi=gi)]
            goods_data.append({
                "goods":goods,
                "gimg":gimg,
                "gdetails":gdetails,
            })
        goodstypes = GoodsType.objects.filter()
        context = {
            "brand":brand,
            "brands":brands,
            "time_t":time_t,
            "times":times,
            "goods_data":goods_data,
            "goodstypes":goodstypes,
            "no_type_num":len(Goods.objects.filter(g_time=time_t,b_brand=brand,g_type=GoodsType.objects.get(gt_type="未分类"))),
        }
        return render(request,"goods_type_upload.html",context=context)

    def post(self,request):
        goods_type = request.POST.get("goodstype")
        g_type = request.POST.get("g_type")
        g_ids = request.POST.getlist("g_id")
        brand = Goods.objects.get(g_id=g_ids[0]).b_brand
        time = Goods.objects.get(g_id=g_ids[0]).g_time
        if g_type == "":
            goodstype = GoodsType.objects.filter(gt_type=goods_type)[0]
        else:
            goodstypes = GoodsType.objects.filter(gt_type=g_type)
            if len(goodstypes) == 0:
                goodstype_id = uuid.uuid1()
                gt = GoodsType()
                gt.gt_id = goodstype_id
                gt.gt_type = g_type
                gt.save()
                goodstype = GoodsType.objects.get(gt_id=goodstype_id)
            elif len(goodstypes) == 1:
                goodstype = goodstypes[0]
        for g_id in g_ids:
            goods = Goods.objects.get(g_id=g_id)
            goods.g_type = goodstype
            goods.save()
        return redirect("/goods_type/goods_type_upload?b_name=%s&t_time=%s" % (brand.b_name, time.t_id))

class BrandGoodsTypeUpload(View):
    """
    品牌产品类型上传
    """
    def get(self,request):
        b_pk = request.GET.get("brand")
        t_pk = request.GET.get("time")
        brand = Brand.objects.get(pk=b_pk)
        time = Time.objects.get(pk=t_pk)
        goodss = Goods.objects.filter(b_brand=brand,g_time=time)
        for goods in goodss:
            if len(BrandGoodsType.objects.filter(bgt_goods_name=goods.g_name)) == 0 and goods.g_type.gt_type != "未分类":
                brandgoodstype = BrandGoodsType()
                brandgoodstype.bgt_id = uuid.uuid1()
                brandgoodstype.bgt_goods_name = goods.g_name
                brandgoodstype.bgt_goods_type = goods.g_type.gt_type
                brandgoodstype.bgt_brand = brand
                brandgoodstype.save()
        return redirect("/goods_type/goods_type_upload?b_name=%s&t_time=%s"%(brand.b_name,time.t_id))

class BrandGoodsTypeClassification(View):
    """
    品牌产品类型自动分类
    """
    def get(self,request):
        b_pk = request.GET.get("brand")
        t_pk = request.GET.get("time")
        brand = Brand.objects.get(pk=b_pk)
        time = Time.objects.get(pk=t_pk)
        goodss = Goods.objects.filter(b_brand=brand, g_time=time)
        for goods in goodss:
            brandgoodstype = BrandGoodsType.objects.filter(bgt_goods_name=goods.g_name,bgt_brand=brand)
            if goods.g_type.gt_type == "未分类" and len(brandgoodstype) == 1:
                goodstype = GoodsType.objects.get(gt_type=brandgoodstype[0].bgt_goods_type)
                goods.g_type = goodstype
                goods.save()
        return redirect("/goods_type/goods_type_upload?b_name=%s&t_time=%s"%(brand.b_name,time.t_id))

class GoodsTypeHandler(View):
    """
    产品类型
    """
    def get(self,request):
        b_name = request.GET.get("b_name")
        brand = Brand.objects.get(b_name=b_name)
        t_time = Time.objects.filter().order_by("-pk")[0]
        goodstypes = GoodsType.objects.filter().order_by("-pk")
        goodstypedatas = [{"goodstype":i,"goodss_len":len(Goods.objects.filter(g_time=t_time,b_brand=brand,g_type=i))} for i in goodstypes]
        goodstypedatas = sorted(goodstypedatas,key=lambda k:k["goodss_len"],reverse=True)
        context = {
            "title":"产品帽型",
            "brand":brand,
            "t_time":t_time,
            "goodstypedatas":goodstypedatas,
        }
        return render(request,"goods_type_top10.html",context=context)

class GoodsTypeList(View):
    def get(self,request):
        title = "产品类型列表"
        b_name = request.GET.get("b_name")
        time_id = request.GET.get("time_id")
        gt_type = request.GET.get("goodstype")
        brand = Brand.objects.get(b_name=b_name)
        t_time = Time.objects.get(t_id=time_id)
        goodstype = GoodsType.objects.get(gt_type=gt_type)
        goodss = Goods.objects.filter(g_time=t_time,b_brand=brand,g_type=goodstype)
        #生成分页对象
        pagenow = int(request.GET.get("pagenow", 1))
        paegsize = 6
        pagintor = Paginator(goodss, paegsize)
        page = pagintor.page(pagenow)

        goods_info = []
        for i in page.object_list:
            goods_info.append({
                "goods_pk": i.pk,
                "goods_name": i.g_name,
                "goods_title": i.g_title,
                "goods_price_type": i.g_price_type,
                "goods_now_price": i.g_now_price,
                "goods_discount_price": i.g_discount_price,
                "goods_image": GoodsImage.objects.filter(gimg_gi_goods=GoodsInformation.objects.filter(gi_goods=i)[0])[
                    0].gimg_path,
                "goods_views": len(BrowseHistory.objects.filter(bh_goods=i)),
                "goods_color_num": len(set([i.gi_color for i in GoodsInformation.objects.filter(gi_goods=i)]))
            })

        page_num = 5
        page_count = pagintor.num_pages
        page_range = pagintor.page_range
        if len(page_range) < page_num:
            pagerange = page_range
        else:
            if 1 <= pagenow <= page_num // 2:
                page_start = 1
                page_end = page_num
            else:
                page_start = pagenow - page_num // 2 + 1
                page_end = pagenow + page_num // 2 + 1

            if page_end > page_count:
                page_end = page_count
            if page_end == page_count:
                page_start = page_count - page_num + 1

            if page_end <= page_num:
                page_end = page_num

            pagerange = [page for page in range(page_start, page_end + 1)]

        context = {
            "title": title,
            "t_time": t_time,
            "goods_info": goods_info,
            "page": page,
            "brand": brand,
            "pagerange": pagerange,
            "pagenow": pagenow,
            "goodstype": goodstype,
        }

        request.session["url_type"] = "type_list"
        return render(request,"goods_type_list.html",context=context)

class GoodsColorTypeUpload(View):
    """
    产品颜色类型上传
    """
    def get(self,request):
        b_name = request.GET.get("b_name", "")
        t_time = request.GET.get("t_time", "")
        brands = Brand.objects.filter().order_by("pk")
        if b_name == "":
            brand = brands[0]
        else:
            brand = Brand.objects.get(b_name=b_name)
        times = Time.objects.filter().order_by("pk")
        if t_time == "":
            time_t = times[0]
        else:
            time_t = Time.objects.get(t_id=t_time)
        goodss = Goods.objects.filter(g_time=time_t, b_brand=brand)
        goodscolortypes = GoodsColorType.objects.filter().order_by("-pk")
        goodscolordatas = []
        for goods in goodss:
            gis = GoodsInformation.objects.filter(gi_goods=goods)
            for gi in gis:
                gimg = GoodsImage.objects.filter(gimg_gi_goods=gi).order_by("pk")[0]
                goodscolordatas.append({
                    "goods":goods,
                    "gi":gi,
                    "gimg":gimg,
                })
        context = {
            "brand":brand,
            "brands":brands,
            "time_t":time_t,
            "times":times,
            "goodscolortypes":goodscolortypes,
            "goodscolordatas":goodscolordatas,
            "no_color_type_num":len([i for i in goodscolordatas if i["gi"].gi_color_type.gct_color_type == "未分类"])
        }
        return render(request,"goods_color_type_upload.html",context=context)

    def post(self,request):
        goods_colortype = request.POST.get("goods_colortype")
        g_colortype = request.POST.get("g_colortype")
        gi_ids = request.POST.getlist("gi_id")
        brand = GoodsInformation.objects.get(gi_id=gi_ids[0]).gi_goods.b_brand
        time = GoodsInformation.objects.get(gi_id=gi_ids[0]).gi_goods.g_time
        if g_colortype == "":
            goodscolortype = GoodsColorType.objects.filter(gct_color_type=goods_colortype)[0]
        else:
            goodscolortypes = GoodsColorType.objects.filter(gct_color_type=g_colortype)
            if len(goodscolortypes) == 0:
                gctype_id = uuid.uuid1()
                gct = GoodsColorType()
                gct.gct_id = gctype_id
                gct.gct_color_type = g_colortype
                gct.save()
                goodscolortype = GoodsColorType.objects.get(gct_id=gctype_id)
            elif len(goodscolortypes) == 1:
                goodscolortype = goodscolortypes[0]
        for gi_id in gi_ids:
            gi = GoodsInformation.objects.get(gi_id=gi_id)
            gi.gi_color_type = goodscolortype
            gi.save()
        return redirect("/goods_type/goods_color_type_upload?b_name=%s&t_time=%s" % (brand.b_name, time.t_id))

class BrandGoodsColorTypeUpload(View):
    """
    品牌产品颜色类型自动上传
    """
    def get(self,request):
        b_pk = request.GET.get("brand")
        t_pk = request.GET.get("time")
        brand = Brand.objects.get(pk=b_pk)
        time = Time.objects.get(pk=t_pk)
        goodss = Goods.objects.filter(b_brand=brand, g_time=time)
        for goods in goodss:
            for goodsinformation in GoodsInformation.objects.filter(gi_goods=goods):
                if len(BrandGoodsColorType.objects.filter(bgct_goods_color=goodsinformation.gi_color)) == 0 and goodsinformation.gi_color_type.gct_color_type != "未分类":
                    brandgoodscolortype = BrandGoodsColorType()
                    brandgoodscolortype.bgct_id = uuid.uuid1()
                    brandgoodscolortype.bgct_goods_color = goodsinformation.gi_color
                    brandgoodscolortype.bgct_goods_color_type = goodsinformation.gi_color_type.gct_color_type
                    brandgoodscolortype.bgct_brand = brand
                    brandgoodscolortype.save()
        return redirect("/goods_type/goods_color_type_upload?b_name=%s&t_time=%s"%(brand.b_name,time.t_id))

class BrandGoodsColorTypeClassification(View):
    """
    品牌产品颜色类型自动分类
    """
    def get(self,request):
        b_pk = request.GET.get("brand")
        t_pk = request.GET.get("time")
        brand = Brand.objects.get(pk=b_pk)
        time = Time.objects.get(pk=t_pk)
        goodss = Goods.objects.filter(b_brand=brand, g_time=time)
        for goods in goodss:
            for goodsinformation in GoodsInformation.objects.filter(gi_goods=goods):
                brandgoodscolortype = BrandGoodsColorType.objects.filter(bgct_goods_color=goodsinformation.gi_color,bgct_brand=brand)
                if goodsinformation.gi_color_type.gct_color_type == "未分类" and len(brandgoodscolortype) == 1:
                    goodscolortype = GoodsColorType.objects.get(gct_color_type=brandgoodscolortype[0].bgct_goods_color_type)
                    goodsinformation.gi_color_type = goodscolortype
                    goodsinformation.save()
        return redirect("/goods_type/goods_color_type_upload?b_name=%s&t_time=%s" % (brand.b_name, time.t_id))

class GoodsColorTypeHandler(View):
    """
    产品颜色类型
    """
    def get(self,request):
        b_name = request.GET.get("b_name")
        brand = Brand.objects.get(b_name=b_name)
        t_time = Time.objects.filter().order_by("-pk")[0]
        goodss = Goods.objects.filter(b_brand=brand,g_time=t_time)
        goodscolortypes = GoodsColorType.objects.filter().order_by("pk")
        goodscolortypedatas = []
        for goodscolortype in goodscolortypes:
            gct_len = sum([len(GoodsInformation.objects.filter(gi_goods=i,gi_color_type=goodscolortype)) for i in goodss])
            goodscolortypedatas.append({
                "gct":goodscolortype,
                "gct_len":gct_len,
            })
        goodscolortypedatas = sorted(goodscolortypedatas, key=lambda k: k["gct_len"], reverse=True)
        context = {
            "title":"产品颜色类型",
            "brand": brand,
            "t_time": t_time,
            "goodscolortypedatas": goodscolortypedatas,
        }
        #撞色
        goodsmatchcolor_len = sum([len(GoodsInformation.objects.filter(gi_goods=i,gi_match_color=True)) for i in goodss])
        context["goodsmatchcolor_len"] = goodsmatchcolor_len
        return render(request,"goods_color_type_top10.html",context=context)

class GoodsColorTypeList(View):
    def get(self,request):
        title = "产品颜色列表"
        b_name = request.GET.get("b_name")
        time_id = request.GET.get("time_id")
        gct_color_type = request.GET.get("gct_color_type")
        brand = Brand.objects.get(b_name=b_name)
        t_time = Time.objects.get(t_id=time_id)
        goodss = Goods.objects.filter(b_brand=brand, g_time=t_time)
        if gct_color_type == "撞色":
            gctype = "撞色"
            gs = []
            for goods in goodss:
                goodsinfos = GoodsInformation.objects.filter(gi_goods=goods,gi_match_color=True)
                if len(goodsinfos) > 0:
                    for goodsinfo in goodsinfos:
                        gs.append({
                             "goods_pk": goods.pk,
                            "gi_pk": goodsinfo.pk,
                            "goods_name": goods.g_name,
                            "goods_title": goods.g_title,
                            "goods_price_type": goods.g_price_type,
                            "goods_now_price": goods.g_now_price,
                            "goods_discount_price": goods.g_discount_price,
                            "goods_image":GoodsImage.objects.filter(gimg_gi_goods=goodsinfo).order_by("pk")[0],
                            "goods_views": len(BrowseHistory.objects.filter(bh_goods=goods)),
                            "goods_color_num": len(set([i.gi_color for i in GoodsInformation.objects.filter(gi_goods=goods)])),
                        })
        else:
            gctype = GoodsColorType.objects.get(gct_color_type=gct_color_type)
            gs = []
            for goods in goodss:
                goodsinfos = GoodsInformation.objects.filter(gi_color_type=gctype,gi_goods=goods)
                for goodsinfo in goodsinfos:
                    gs.append({
                        "goods_pk": goods.pk,
                        "gi_pk": goodsinfo.pk,
                        "goods_name": goods.g_name,
                        "goods_title": goods.g_title,
                        "goods_price_type": goods.g_price_type,
                        "goods_now_price": goods.g_now_price,
                        "goods_discount_price": goods.g_discount_price,
                        "goods_image":GoodsImage.objects.filter(gimg_gi_goods=goodsinfo).order_by("pk")[0],
                        "goods_views": len(BrowseHistory.objects.filter(bh_goods=goods)),
                        "goods_color_num": len(set([i.gi_color for i in GoodsInformation.objects.filter(gi_goods=goods)])),
                    })
        # 生成分页对象
        pagenow = int(request.GET.get("pagenow", 1))
        paegsize = 6
        pagintor = Paginator(gs, paegsize)
        page = pagintor.page(pagenow)

        goods_info = page.object_list
        page_num = 5
        page_count = pagintor.num_pages
        page_range = pagintor.page_range
        if len(page_range) < page_num:
            pagerange = page_range
        else:
            if 1 <= pagenow <= page_num // 2:
                page_start = 1
                page_end = page_num
            else:
                page_start = pagenow - page_num // 2 + 1
                page_end = pagenow + page_num // 2 + 1

            if page_end > page_count:
                page_end = page_count
            if page_end == page_count:
                page_start = page_count - page_num + 1

            if page_end <= page_num:
                page_end = page_num

            pagerange = [page for page in range(page_start, page_end + 1)]

        context = {
            "title": title,
            "t_time": t_time,
            "goods_info": goods_info,
            "page": page,
            "brand": brand,
            "pagerange": pagerange,
            "pagenow": pagenow,
            "gctype": gctype,
        }

        request.session["url_type"] = "type_color_list"
        return render(request,"goods_color_type_list.html",context=context)