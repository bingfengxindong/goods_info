from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.base import View
from django.core.paginator import Paginator
from goods.goods_query_view import *
from goods.update_goods_data import *
from goods_change.models import *
import uuid
import os
import datetime
import json
# Create your views here.

def date_str(date):
    """
    转换时间格式
    :param date:
    :return:
    """
    return str(date.replace("年","-").replace("月","-").replace("日",""))

def str_date(date):
    """
    转换时间格式
    :param date:
    :return:
    """
    return str(date.replace("-","年").replace("-","月").replace("-","日"))

def date_conversion(time_d):
    """
    将时间目录转化为时间
    :param time_dir:
    :return:
    """
    time_dir = [int(i) for i in time_d.split("-")]
    brand_time = datetime.date(time_dir[0], time_dir[1], time_dir[2])
    return brand_time

class GoodsUpload(View):
    """
    查看上传目录内是否有未上传的文件
    """
    def get(self,request):
        upload_dirs = os.path.join(BASE_DIR,"upload_data","data")
        brand_path_list = []
        for upload_dir_name in os.listdir(upload_dirs): #遍历以时间为目录名的的数据目录
            brand_time = date_conversion(upload_dir_name)
            brand_paths = []
            for upload_file_name in os.listdir(os.path.join(upload_dirs,upload_dir_name)): #遍历单个时间目录下的数据文件
                brand_name = upload_file_name.split(".")[0]
                brand = Brand.objects.filter(b_name=brand_name)
                if len(brand) == 1:
                    brandtime = BrandTime.objects.filter(bt_brand=brand[0],bt_time=brand_time)
                    if len(brandtime) == 0:
                        brand_paths.append({
                            "brand_name":brand_name,
                            "brand_path":os.path.join(os.path.join(upload_dirs,upload_dir_name,upload_file_name)),
                            })
                else:
                    brand_paths.append({
                        "brand_name": brand_name,
                        "brand_path": os.path.join(os.path.join(upload_dirs, upload_dir_name, upload_file_name)),
                    })
            brand_path_list.append({
                "time":brand_time,
                "brand_paths":brand_paths,
            })

        context = {
            "title":"产品上传",
            "brand_path_list":brand_path_list,
        }
        return render(request,"goods_upload_data.html",context)

    def post(self,request):
        """
        提交数据文件路径，上传数据
        :param request:
        :return:
        """
        brand_paths = request.POST.getlist("brand_path")
        if brand_paths:
            for brand_path in brand_paths:
                UpdateGoodsDate(brand_path)
        return HttpResponse("%s-ok"%brand_path)

class Index(View):
    """
    首页
    """
    def get(self,request):
        title = "首页"
        brand_types = BrandType.objects.all()
        brand_infos = []
        for brand_type in brand_types:
            brands = Brand.objects.filter(b_bt=brand_type)
            brand_infos.append({
                "brand_type":brand_type,
                "brands":brands,
            })
        context = {
            "title":title,
            "brand_infos":brand_infos,
        }


        username = request.session.get("username")
        u_login_name = request.session.get("u_login_name")
        if username and u_login_name:
            # 浏览历史
            is_or_not_login = 1
            user = User.objects.get(u_login_name=u_login_name)
            # browsehistorys = BrowseHistory.objects.filter(bh_user=user).order_by("-pk")[0:5]
            # goods_infos = [GoodsInformation.objects.filter(gi_goods=i.bh_goods).order_by("pk")[0] for i in browsehistorys]
            # goods_images = [GoodsImage.objects.filter(gimg_gi_goods=i).order_by("pk")[0] for i in goods_infos]
            context["is_or_not_login"] = is_or_not_login
            # context["goods_images_len"] = len(goods_images)
            # context["goods_images"] = goods_images

            #标签
            goodslables = GoodsLable.objects.filter(gl_user=user).order_by("-pk")[0:10]
            context["goodslables_len"] = len(goodslables)
            context["goodslables"] = goodslables

            #自定义描述
            goodsdescs = GoodsCustomDescription.objects.filter(gcd_user=user).order_by("-pk")[0:10]
            context["goodsdescs_len"] = len(goodsdescs)
            context["goodsdescs"] = goodsdescs
        else:
            is_or_not_login = 0
            context["is_or_not_login"] = is_or_not_login


        request.session["url_type"] = "index"
        return render(request,"index.html",context=context)

class GoodsList(View):
    """
    产品列表
    """
    def get(self,request):
        title = "产品列表"
        b_name = request.GET.get("b_name")
        time_id = request.GET.get("time_id","")
        brand = Brand.objects.get(b_name=b_name)
        goods_all = Goods.objects.filter(b_brand=brand)
        #查询该品牌所有的产品时间和某一时间所有产品
        goodstimequery = goods_time_query(goods_all,time_id)
        times = goodstimequery["times"]
        goods_now_time = goodstimequery["goods_now_time"]
        goodss = Goods.objects.filter(b_brand=brand,g_time=goods_now_time)
        #生成分页对象
        pagenow = int(request.GET.get("pagenow",1))
        paegsize = 12
        pagintor = Paginator(goodss,paegsize)
        page = pagintor.page(pagenow)

        goods_info = []
        user = User.objects.filter(u_login_name=request.session.get("u_login_name"))
        for i in page.object_list:
            if len(user) == 0:
                g_col = "logout"
            else:
                goods_col = GoodsCollection.objects.filter(gc_goods=i,gc_user=user[0],isdelete=False)
                if len(goods_col) == 0:
                    g_col = 0
                else:
                    g_col = 1
            goods_info.append({
                "goods_pk":i.pk,
                "goods_name":i.g_name,
                "goods_title":i.g_title,
                "goods_price_type":i.g_price_type,
                "goods_now_price": i.g_now_price,
                "goods_discount_price":i.g_discount_price,
                "goods_image":GoodsImage.objects.filter(gimg_gi_goods=GoodsInformation.objects.filter(gi_goods=i)[0])[0].gimg_path,
                "goods_views":len(BrowseHistory.objects.filter(bh_goods=i)),
                "goods_color_num":len(set([i.gi_color for i in GoodsInformation.objects.filter(gi_goods=i)])),
                "g_col":g_col,
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
            "title":title,
            "goods_now_time":goods_now_time,
            "times":times,
            "goods_info":goods_info,
            "page":page,
            "brand":brand,
            "pagerange":pagerange,
            "pagenow":pagenow,
        }

        request.session["url_type"] = "list"
        return render(request,"goods_list.html",context=context)


class GoodsDetailHandler(View):
    """
    产品详情
    """
    def get(self,request):
        context = {"title":"产品详情"}
        goods_pk = int(request.GET.get("goods_pk"))
        color_pk = request.GET.get("color_pk","")
        goods = Goods.objects.get(pk=goods_pk)
        goodss = [i for i in Goods.objects.filter(b_brand=goods.b_brand,g_time=goods.g_time)]
        g_index = goodss.index(goods)
        if g_index == 0:
            old_goods = 0
            next_goods = goodss[goodss.index(goods) + 1]
        elif g_index == len(goodss) - 1:
            old_goods = goodss[goodss.index(goods) - 1]
            next_goods = 0
        else:
            old_goods = goodss[goodss.index(goods) - 1]
            next_goods = goodss[goodss.index(goods) + 1]
        context["old_goods"] = old_goods
        context["next_goods"] = next_goods

        goodsinformations = GoodsInformation.objects.filter(gi_goods=goods)
        if color_pk == "":
            goodsinformation = goodsinformations[0]
        else:
            goodsinformation = GoodsInformation.objects.get(pk=color_pk)
        goodssizes = GoodsSize.objects.filter(gs_gi=goodsinformation)
        goodsdetails = GoodsDetail.objects.filter(gd_gi=goodsinformation)
        goodsimages = GoodsImage.objects.filter(gimg_gi_goods=goodsinformation)
        brand = goods.b_brand
        #该产品所有型号的第一张图片
        goods_first_images = []
        for goodsinfo in goodsinformations:
            gimage = GoodsImage.objects.filter(gimg_gi_goods=goodsinfo)[0]
            goods_first_images.append({
                "color_pk":goodsinfo.pk,
                "gimg_path":gimage.gimg_path,
            })
        context["goods_first_images"] = goods_first_images
        context["goodsinformation"] = goodsinformation
        context["goods_sizes"] = goodssizes
        context["goods_details"] = goodsdetails
        context["goods_details_len"] = len(goodsdetails)
        context["goods_images"] = goodsimages

        goods_change = GoodsPriceChange.objects.filter(gpc_now_goods=goods,gpc_time=goods.g_time)
        if len(goods_change) == 0:
            context["goods_change_len"] = 0
            context["change"] = 0
        else:
            if goods_change[0].gpc_price_state == 1:
                context["goods_change"] = goods_change[0]
                context["goods_change_len"] = 1
                context["change"] = "up"
            elif goods_change[0].gpc_price_state == 2:
                context["goods_change"] = goods_change[0]
                context["goods_change_len"] = 1
                context["change"] = "down"


        username = request.session.get("username")
        u_login_name = request.session.get("u_login_name")
        if username and u_login_name:
            is_or_not_login = 1

            user = User.objects.get(u_login_name=u_login_name)
            #标签
            goodslables = GoodsLable.objects.filter(gl_goods=goods,gl_user=user,isdelete=False).order_by("-pk")
            if len(goodslables) == 0:
                gla = 0
                lable = "该商品无标签，请添加！"
                context["lable"] = lable
            else:
                gla = 1
                if len(goodslables) <= 3:
                    lables = goodslables
                else:
                    lables = goodslables[0:3]
                context["lables"] = lables[:30]

            #自定义描述
            # goodscustomdescshiss = GoodsCustomDescription.objects.filter(gcd_goods=goods,gcd_user=user).order_by("-pk")
            goodscustomdescs = GoodsCustomDescription.objects.filter(gcd_goods=goods,gcd_user=user,isdelete=False).order_by("-pk")
            if len(goodscustomdescs) == 0:
                gcd_n = 0
            else:
                gcd_n = 1
                goodscustomdesc = goodscustomdescs[0]
                context["goodscustomdesc"] = goodscustomdesc
            context["goodscustomdescshiss"] = goodscustomdescs[:30]

            #添加至浏览历史
            if "url_type" in request.session:
                if request.session["url_type"] == "list":
                    browsehistory = BrowseHistory()
                    browsehistory.bh_id = str(uuid.uuid1())
                    browsehistory.bh_goods = goods
                    browsehistory.bh_user = user
                    browsehistory.save()

            #收藏
            goods_collects = GoodsCollection.objects.filter(gc_goods=goods,gc_user=user,isdelete=False)
            if len(goods_collects) == 0:
                col = 0
            elif len(goods_collects) == 1:
                col = 1

            context["gla"] = gla
            context["goodslables"] = goodslables
            context["col"] = col
            context["gcd_n"] = gcd_n
        else:
            is_or_not_login = 0
        context["is_or_not_login"] = is_or_not_login

        #评论
        goods_comments = GoodsComment.objects.filter(gc_goods=goods)
        if len(goods_comments) == 0:
            context["goods_comments_len"] = "0"
        else:
            context["goods_comments_len"] = "1"
            g_comments = []
            for goods_comment in goods_comments:
                star1 = ""
                star2 = ""
                for i1 in range(goods_comment.gc_comment_star):
                    star1 += '<span class="glyphicon glyphicon-star" aria-hidden="true"></span>'
                for i2 in range(5-goods_comment.gc_comment_star):
                    star2 += '<span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>'
                star = star1 + star2
                g_comments.append({
                    "gcom_time":goods_comment.gc_comment_time,
                    "gcom_comment":goods_comment.gc_comment,
                    "gcom_star":star,
                })
            context["goods_comments"] = g_comments

        context["brand"] = brand
        context["goods"] = goods

        request.session["url_type"] = "detail"
        return render(request,"goods_detail.html",context=context)

    def post(self,request):
        gi_model = request.POST.get("gi_model")
        gi_gender = request.POST.get("gi_gender")
        goodsinformations = GoodsInformation.objects.filter(gi_model=gi_model,gi_gender=gi_gender)
        gis = [{"gi_model":i.gi_model,"gi_order":i.gi_order,"gi_gender":gi_gender,"time":str(i.gi_goods.g_time.t_time)} for i in goodsinformations]
        return HttpResponse(json.dumps(gis))

class GoodsImageHandler(View):
    """
    大图加载
    """
    def post(self,request):
        gi_pk = request.POST.get("gi_pk","")
        gimg_pk = request.POST.get("gimg_pk","")
        if gi_pk == "":
            goodsimage = GoodsImage.objects.get(pk=gimg_pk)
            gimg_path = goodsimage.gimg_path
        else:
            goodsinfo = GoodsInformation.objects.get(pk=gi_pk)
            goodsimage = GoodsImage.objects.filter(gimg_gi_goods=goodsinfo)[0]
            gimg_path = goodsimage.gimg_path
        return HttpResponse(gimg_path)

class GoodsCollectionHandler(View):
    """
    收藏
    取消收藏
    """
    def get(self,request):
        goods_id = request.GET.get("goods_id")
        goods = Goods.objects.get(g_id=goods_id)
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        goods_collects = GoodsCollection.objects.filter(gc_goods=goods,gc_user=user)
        if len(goods_collects) == 0:
            col = 0
            gc_id = str(uuid.uuid1())
            goods_col = GoodsCollection()
            goods_col.gc_id = gc_id
            goods_col.gc_collection = 1
            goods_col.gc_goods = goods
            goods_col.gc_user = user
            goods_col.save()
        else:
            for goods_collect in goods_collects:
                if goods_collect.gc_collection == 1 and goods_collect.isdelete == False:
                    col = 1
                    break
            else:
                col = 0
                gc_id = str(uuid.uuid1())
                goods_col = GoodsCollection()
                goods_col.gc_id = gc_id
                goods_col.gc_collection = 1
                goods_col.gc_goods = goods
                goods_col.gc_user = user
                goods_col.save()
        return HttpResponse(col)

    def post(self,request):
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.get(g_id=goods_id)
        goods_collects = GoodsCollection.objects.filter(gc_goods=goods)
        for goods_collect in goods_collects:
            goods_collect.isdelete = True
            goods_collect.save()
        return HttpResponse("ok")

class GoodsLableHandler(View):
    """
    产品标签添加，删除
    """
    def post(self,request):
        """添加"""
        goods_id = request.POST.get("goods_id")
        goods_lable = request.POST.get("goods_lable")
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        goods = Goods.objects.get(g_id=goods_id)
        gl = GoodsLable.objects.filter(gl_lable=goods_lable,gl_goods=goods)
        if len(gl) == 1 and gl[0].isdelete == False:
            return redirect("/goods/goods_detail?goods_pk=%s"%goods.pk)
        elif len(gl) == 1 and gl[0].isdelete == True:
            goodslable = gl[0]
            goodslable.isdelete = False
            goodslable.save()
        else:
            goodslable = GoodsLable()
            goodslable.gl_id = str(uuid.uuid1())
            goodslable.gl_lable = goods_lable
            goodslable.gl_goods = goods
            goodslable.gl_user = user
            goodslable.save()
        return redirect("/goods/goods_detail?goods_pk=%s"%goods.pk)

    def get(self,request):
        """删除"""
        gl_pk = request.GET.get("gl_pk")
        goodslable = GoodsLable.objects.get(pk=gl_pk)
        goods_pk = goodslable.gl_goods.pk
        goodslable.isdelete = True
        goodslable.save()
        return redirect("/goods/goods_detail?goods_pk=%s"%goods_pk)

class GoodsLableEditHandler(View):
    def get(self,request):
        edit_lable = request.GET.get("edit_lable")
        lable_id = request.GET.get("lable_id")
        lable = GoodsLable.objects.get(gl_id=lable_id)
        lable.gl_lable = edit_lable
        lable.save()
        return HttpResponse(lable.gl_lable)

class GoodsDescHandler(View):
    """
    用户自定义描述
    """
    def get(self,request):
        """
        删除描述
        :param request:
        :return:
        """
        pk = request.GET.get("desc_pk")
        goods_pk = request.GET.get("goods_pk")
        goodscustomdesc = GoodsCustomDescription.objects.get(pk=pk)
        goodscustomdesc.isdelete = True
        goodscustomdesc.save()
        return redirect("/goods/goods_detail?goods_pk=%s"%goods_pk)

    def post(self,request):
        """
        添加描述
        :param request:
        :return:
        """
        goods_id = request.POST.get("goods_id")
        goods_desc = request.POST.get("goods_desc")
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        goods = Goods.objects.get(g_id=goods_id)
        goodscustomdesc = GoodsCustomDescription()
        goodscustomdesc.gcd_id = str(uuid.uuid1())
        goodscustomdesc.gcd_description = goods_desc
        goodscustomdesc.gcd_goods = goods
        goodscustomdesc.gcd_user = user
        goodscustomdesc.save()
        return redirect("/goods/goods_detail?goods_pk=%s"%goods.pk)

class GoodsDescEditHandler(View):
    """
    产品描述修改
    """
    def get(self,request):
        edit_gcd = request.GET.get("edit_gcd")
        gcd_id = request.GET.get("gcd_id")
        gcd = GoodsCustomDescription.objects.get(gcd_id=gcd_id)
        gcd.gcd_description = edit_gcd
        gcd.save()
        data = "%s：%s"%(gcd.create_date,edit_gcd)
        return HttpResponse(data)

class GoodsStarHandler(View):
    """
    打开页面后异步刷新星级
    异步修改星级
    """
    def get(self,request):
        num = request.GET.get("num")
        goods_id = request.GET.get("goods_id")
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        goods = Goods.objects.get(g_id=goods_id)
        goodsstar = GoodsStar()
        goodsstar.gs_id = str(uuid.uuid1())
        goodsstar.gs_star = int(num)
        goodsstar.gs_goods = goods
        goodsstar.gs_user = user
        goodsstar.save()
        return HttpResponse("ok")

    def post(self,request):
        goods_id = request.POST.get("goods_id")
        u_login_name = request.session.get("u_login_name")
        if u_login_name:
            user = User.objects.get(u_login_name=u_login_name)
            goods = Goods.objects.get(g_id=goods_id)
            goodsstars = GoodsStar.objects.filter(gs_goods=goods,gs_user=user).order_by("-pk")
            if len(goodsstars) == 0:
                data = 0
            else:
                data = goodsstars[0].gs_star
        else:
            data = 0
        return HttpResponse(data)