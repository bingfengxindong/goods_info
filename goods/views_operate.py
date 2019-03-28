from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from goods_change.models import *
from .models import *
from .views import date_str
from user.views import login_verify


class GoodsAnalysisTop10(View):
    """
    产品分析top10
    """
    def get(self,request):
        b_name = request.GET.get("b_name")
        brand = Brand.objects.get(b_name=b_name)
        times = Time.objects.filter().order_by("-pk")[0]
        goodss = Goods.objects.filter(b_brand=brand,g_time=times)
        goodsinforamtionall = []
        for goods in goodss:
            goodsinforamtions = GoodsInformation.objects.filter(gi_goods=goods).order_by("gi_order")
            for goodsinforamtion in goodsinforamtions:
                goodsinforamtionall.append(goodsinforamtion)

        goods_pages = list(set([i.gi_page for i in goodsinforamtionall]))
        go_page = request.GET.get("goods_page","")
        if go_page == "":
            goods_page = goods_pages[0]
        else:
            goods_page = int(go_page)

        goodsinforamtionallones = []
        for goods in goodss:
            goodsinforamtionones = GoodsInformation.objects.filter(gi_goods=goods,gi_page=goods_page)
            if len(goodsinforamtionones) != 0:
                for goodsinforamtionone in goodsinforamtionones:
                    goodsinforamtionallones.append({
                        "pk":goodsinforamtionone.pk,
                        "gi_id":goodsinforamtionone.gi_id,
                        "gi_model":goodsinforamtionone.gi_model,
                        "gi_img":GoodsImage.objects.filter(gimg_gi_goods=goodsinforamtionone)[0],
                        "gi_gender":goodsinforamtionone.gi_gender,
                        "gi_order":goodsinforamtionone.gi_order,
                        "gi_page":goodsinforamtionone.gi_page,
                        "gi_goods":goodsinforamtionone.gi_goods,
                    })
                goodsinforamtionallones = sorted(goodsinforamtionallones, key=lambda k: k["pk"])
        if len(goodsinforamtionallones) <= 10:
            goodsinforamtionallones = sorted(goodsinforamtionallones,key=lambda k:k["gi_order"])
        else:
            goodsinforamtionallones = sorted(goodsinforamtionallones, key=lambda k:k["gi_order"])

        datas = []
        for goodsinforamtionallone in goodsinforamtionallones:
            goodsorderchange = GoodsOrderChange.objects.filter(goc_now_goods=goodsinforamtionallone["gi_goods"],goc_now_time=times.t_time)
            if len(goodsorderchange) != 0:
                goodsorderchangechange = GoodsOrderChangeChange.objects.filter(goocc_goc=goodsorderchange[0],gocc_now_order=goodsinforamtionallone["gi_order"],gocc_page=goodsinforamtionallone["gi_page"]).order_by("pk")
                goodsinforamtionallone["goodsorderchange"] = "true"
                if len(goodsorderchangechange) != 0:
                    goodsinforamtionallone["goodsorderchangechange"] = goodsorderchangechange[0]
                else:
                    goodsinforamtionallone["goodsorderchangechange"] = "none"
            else:
                goodsinforamtionallone["goodsorderchange"] = "false"
            # print(goodsordertop10one)
            datas.append(goodsinforamtionallone)

        ga_type = request.GET.get("type","")
        if ga_type == "":
            context = {
                "title":"产品位置分析top10",
                "brand":brand,
                "time":times,
                "goods_pages":goods_pages,
                "goods_page":goods_page,
                "goodsinforamtionallones":goodsinforamtionallones,
                "datas":datas[:10],
                "type":"ten",
            }
        elif ga_type == "all":
            context = {
                "title": "产品位置分析",
                "brand": brand,
                "time": times,
                "goods_pages": goods_pages,
                "goods_page": goods_page,
                "goodsinforamtionallones": goodsinforamtionallones,
                "datas": datas,
                "type": "all",
            }

        request.session["url_type"] = "list"
        return render(request,"goods_analysis_top10.html",context=context)

class ProductAnalysis(View):
    """
    产品变化数据
    """
    def get(self,request):
        analysis_type = request.GET.get("analysis_type","price")
        now_time_id = request.GET.get("now_time","")
        times = [i for i in Time.objects.filter().order_by("-pk")][:-1]
        context = {"title":"产品分析"}
        if analysis_type:
            func = getattr(self,analysis_type)
            func(now_time_id,context,times,analysis_type)

            request.session["url_type"] = "analysis"
            return render(request, "product_analysis.html", context=context)

    @staticmethod
    def price(now_time_id,context,times,analysis_type):
        """
        价格变化数据
        :param context:
        :return:
        """
        if now_time_id == "":
            price_rising_changes = GoodsPriceChange.objects.filter(gpc_time=times[0], gpc_price_state=1)
            price_falling_changes = GoodsPriceChange.objects.filter(gpc_time=times[0], gpc_price_state=2)
            now_time = times[0].t_id
        else:
            price_rising_changes = GoodsPriceChange.objects.filter(gpc_time=Time.objects.get(t_id=now_time_id),
                                                                   gpc_price_state=1)
            price_falling_changes = GoodsPriceChange.objects.filter(gpc_time=Time.objects.get(t_id=now_time_id),
                                                                    gpc_price_state=2)
            now_time = now_time_id
        now_times = Time.objects.get(t_id=now_time)
        context["times"] = times
        context["now_times"] = now_times
        context["now_time_id"] = now_time
        context["analysis_type"] = analysis_type
        context["price_rising_changes"] = price_rising_changes
        context["price_rising_changes_len"] = len(price_rising_changes)
        context["price_falling_changes"] = price_falling_changes
        context["price_falling_changes_len"] = len(price_falling_changes)
        return context

    @staticmethod
    def extence(now_time_id,context,times,analysis_type):
        """
        上下架数据
        :return:
        """
        if now_time_id == "":
            shelves_goodss = GoodsExtenceChange.objects.filter(gec_extence_now_time=times[0].t_time,gec_extence_type=2)
            the_shelves_goodss = GoodsExtenceChange.objects.filter(gec_extence_now_time=times[0].t_time,gec_extence_type=1)
            now_time = times[0].t_id
        else:
            shelves_goodss = GoodsExtenceChange.objects.filter(gec_extence_now_time=Time.objects.get(t_id=now_time_id).t_time,gec_extence_type=2)
            the_shelves_goodss = GoodsExtenceChange.objects.filter(gec_extence_now_time=Time.objects.get(t_id=now_time_id).t_time,gec_extence_type=1)
            now_time = now_time_id
        now_times = Time.objects.get(t_id=now_time)
        context["times"] = times
        context["now_times"] = now_times
        context["now_time_id"] = now_time
        context["analysis_type"] = analysis_type
        context["shelves_goodss"] = shelves_goodss
        context["shelves_goodss_len"] = len(shelves_goodss)
        context["the_shelves_goodss"] = the_shelves_goodss
        context["the_shelves_goodss_len"] = len(the_shelves_goodss)
        return context

    @staticmethod
    def order(now_time_id,context,times,analysis_type):
        """
        位置变化数据
        :param now_time_id:
        :param context:
        :param times:
        :param analysis_type:
        :return:
        """
        #位置变化品牌
        if now_time_id == "":
            order_goodss = GoodsOrderChange.objects.filter(goc_now_time=times[0].t_time)
            now_time = times[0].t_id
        else:
            order_goodss = GoodsOrderChange.objects.filter(goc_now_time=Time.objects.get(t_id=now_time_id).t_time)
            now_time = now_time_id
        raising_datas = []
        falling_datas = []
        for order_goods in order_goodss:
            #上升
            raising_goods_orders = []
            goods_order_changes_raising = GoodsOrderChangeChange.objects.filter(goocc_goc=order_goods,gocc_order_state=1)
            if len(goods_order_changes_raising) != 0:
                for goods_order_change_raising in goods_order_changes_raising:
                    raising_goods_orders.append({
                        "gi":GoodsInformation.objects.get(gi_id=goods_order_change_raising.gocc_now_goods_id),
                        "previous_order":goods_order_change_raising.gocc_previous_order,
                        "now_order":goods_order_change_raising.gocc_now_order,
                        "order_change":goods_order_change_raising.gocc_order_change,
                        "order_state":goods_order_change_raising.gocc_order_state,
                        "sex":goods_order_change_raising.gocc_sex,
                    })
                raising_datas.append({
                    "previous_goods":order_goods.goc_previous_goods,
                    "now_goods":order_goods.goc_now_goods,
                    "times":order_goods.goc_now_time,
                    "raising_goods_orders_len":len(goods_order_changes_raising),
                    "raising_goods_orders":raising_goods_orders,
                })
            #下降
            falling_goods_orders = []
            goods_order_changes_falling = GoodsOrderChangeChange.objects.filter(goocc_goc=order_goods,gocc_order_state=2)
            if len(goods_order_changes_falling) != 0:
                for goods_order_change_falling in goods_order_changes_falling:
                    falling_goods_orders.append({
                        "gi": GoodsInformation.objects.get(gi_id=goods_order_change_falling.gocc_now_goods_id),
                        "previous_order": goods_order_change_falling.gocc_previous_order,
                        "now_order": goods_order_change_falling.gocc_now_order,
                        "order_change": goods_order_change_falling.gocc_order_change,
                        "order_state": goods_order_change_falling.gocc_order_state,
                        "sex": goods_order_change_falling.gocc_sex,
                    })
                falling_datas.append({
                    "previous_goods": order_goods.goc_previous_goods,
                    "now_goods": order_goods.goc_now_goods,
                    "times": order_goods.goc_now_time,
                    "falling_goods_orders_len": len(goods_order_changes_falling),
                    "falling_goods_orders": falling_goods_orders,
                })
        now_times = Time.objects.get(t_id=now_time)
        context["times"] = times
        context["now_times"] = now_times
        context["now_time_id"] = now_time
        context["analysis_type"] = analysis_type
        context["raising_datas"] = raising_datas
        context["raising_datas_len"] = len(raising_datas)
        context["falling_datas"] = falling_datas
        context["falling_datas_len"] = len(falling_datas)
        return context

    @staticmethod
    def color(now_time_id,context,times,analysis_type):
        """
        颜色变化数据
        :param now_time_id:
        :param context:
        :param times:
        :param analysis_type:
        :return:
        """
        #颜色变化的产品
        if now_time_id == "":
            goods_color_changes_raising = GoodsColorChange.objects.filter(gcc_time=times[0].t_time,gcc_change_color_state=1)
            goods_color_changes_falling = GoodsColorChange.objects.filter(gcc_time=times[0].t_time,gcc_change_color_state=2)
            now_time = times[0].t_id
        else:
            goods_color_changes_raising = GoodsColorChange.objects.filter(gcc_time=Time.objects.get(t_id=now_time_id).t_time, gcc_change_color_state=1)
            goods_color_changes_falling = GoodsColorChange.objects.filter(gcc_time=Time.objects.get(t_id=now_time_id).t_time, gcc_change_color_state=2)
            now_time = now_time_id
        #颜色上升
        color_raising_datas = []
        for goods_color_change_raising in goods_color_changes_raising:
            goods_change_colors = GoodsColorChangeColor.objects.filter(gccc_goodscolorchange=goods_color_change_raising)
            color_raising_datas.append({
                "change_color_num":goods_color_change_raising.gcc_change_color_num,
                "change_color_state":goods_color_change_raising.gcc_change_color_state,
                "previous_goods":goods_color_change_raising.gcc_previous_goods,
                "now_goods":goods_color_change_raising.gcc_now_goods,
                "times":goods_color_change_raising.gcc_time,
                "goods_change_colors":goods_change_colors,
            })
        #颜色下降
        color_falling_datas = []
        for goods_color_change_falling in goods_color_changes_falling:
            goods_change_colors = GoodsColorChangeColor.objects.filter(gccc_goodscolorchange=goods_color_change_falling)
            color_falling_datas.append({
                "change_color_num": goods_color_change_falling.gcc_change_color_num,
                "change_color_state": goods_color_change_falling.gcc_change_color_state,
                "previous_goods": goods_color_change_falling.gcc_previous_goods,
                "now_goods": goods_color_change_falling.gcc_now_goods,
                "times": goods_color_change_falling.gcc_time,
                "goods_change_colors": goods_change_colors,
            })
        now_times = Time.objects.get(t_id=now_time)
        context["times"] = times
        context["now_times"] = now_times
        context["now_time_id"] = now_time
        context["analysis_type"] = analysis_type
        context["color_raising_datas"] = color_raising_datas
        context["color_raising_datas_len"] = len(color_raising_datas)
        context["color_falling_datas"] = color_falling_datas
        context["color_falling_datas_len"] = len(color_falling_datas)
        return context

class GoodsHistory(View):
    @login_verify
    def get(self,request):
        title = "历史记录"
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        browsehistorys = BrowseHistory.objects.filter(bh_user=user).order_by("pk")
        bh_len = len(browsehistorys)
        if bh_len != 0:
            time_dates = []
            for browsehistory in browsehistorys:
                time_dates.append(browsehistory.create_date)
            time_dates = [i.strftime("%Y-%m-%d") for i in sorted(list(set(time_dates)),reverse=True)]
            now_time = request.GET.get("now_time")
            brand_pk = request.GET.get("brand_pk","")
            brands = Brand.objects.filter().order_by("pk")
            if brand_pk == "":
                brand_now = Brand.objects.filter().order_by("pk")[0]
            else:
                brand_now = Brand.objects.filter(pk=brand_pk)[0]
            if now_time:
                now_time = date_str(now_time)
                browsehistory = [i for i in BrowseHistory.objects.filter(create_date=now_time,bh_user=user).order_by("pk") if i.bh_goods.b_brand == brand_now]
            else:
                now_time = time_dates[0]
                browsehistory = [i for i in BrowseHistory.objects.filter(create_date=now_time,bh_user=user).order_by("pk") if i.bh_goods.b_brand == brand_now]

            #产品信息
            bh_infos = []
            for bhistory in browsehistory:
                goodsinfo = GoodsInformation.objects.filter(gi_goods=bhistory.bh_goods)[0]
                gimg = GoodsImage.objects.filter(gimg_gi_goods=goodsinfo)[0]
                bh_infos.append({
                    "goods":bhistory.bh_goods,
                    "g_img":gimg.gimg_path,
                })

            #品牌与其对应的历史记录数量
            brand_nums = []
            for brand in brands:
                browsehistory_gs = [i for i in BrowseHistory.objects.filter(create_date=now_time,bh_user=user).order_by("pk")if i.bh_goods.b_brand == brand]
                brand_nums.append({
                    "brand":brand,
                    "num":len(browsehistory_gs),
                })
            context = {
                "title":title,
                "now_time":now_time,
                "time_dates":time_dates,
                "brand_nums":brand_nums,
                "brand":brand_now,
                "browsehistorys":browsehistory,
                "bh_infos":bh_infos,
                "bh_single_len":len(browsehistory),
                "bh_len":bh_len,
            }
        else:
            context = {
                "title":title,
                "content":"当前无用户浏览历史记录！",
                "bh_len": bh_len,
            }

        request.session["url_type"] = "history"
        return render(request,"goods_history.html",context=context)

class UserCenterInfo(View):
    """
    用户个人中心 用户信息
    """
    def get(self,request):
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        context = {
            "title":"用户个人中心-用户信息",
            "user":user,
        }
        return render(request, "user_center_info.html", context=context)

class UserCenterCol(View):
    """
    用户个人中心 用户收藏记录
    """
    def get(self,request):
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        goodscollection = [i for i in GoodsCollection.objects.filter(gc_user=user).order_by("-pk")]
        gc_times = sorted(list(set([i.create_date for i in goodscollection])),reverse=True)
        print(gc_times)
        gcs = [[] for i in gc_times]
        for gc_time in gc_times:
            for gcol in goodscollection:
                if gc_time == gcol.create_date:
                    gimg = GoodsImage.objects.filter(gimg_gi_goods=GoodsInformation.objects.filter(gi_goods=gcol.gc_goods)[0])[0]
                    gcs[gc_times.index(gc_time)].append({"goods":gcol.gc_goods,"gimg":gimg})
        goodscols = []
        for gc in gcs:
            goodscols.append({
                "time":gc_times[gcs.index(gc)],
                "goods_data":gc,
            })
        context = {
            "title": "用户个人中心-收藏记录",
            "goodscols":goodscols,
        }
        return render(request, "user_center_col.html", context=context)

class UserCenterHistory(View):
    """
    用户个人中心 用户历史浏览记录
    """
    def get(self,request):
        u_login_name = request.session.get("u_login_name")
        user = User.objects.get(u_login_name=u_login_name)
        browsehistorys = BrowseHistory.objects.filter(bh_user=user)
        bh_times = sorted(list(set([i.create_date for i in browsehistorys])),reverse=True)[:10]
        bhs = [[] for i in bh_times]
        for bh_time in bh_times:
            for browsehistory in browsehistorys:
                if bh_time == browsehistory.create_date:
                    gimg = GoodsImage.objects.filter(gimg_gi_goods=GoodsInformation.objects.filter(gi_goods=browsehistory.bh_goods)[0])[0]
                    bhs[bh_times.index(bh_time)].append({"goods":browsehistory.bh_goods,"gimg":gimg})
        goodshistorys = []
        for bh in bhs:
            goodshistorys.append({
                "time": bh_times[bhs.index(bh)],
                "goods_data": bh,
            })
        context = {
            "title": "用户个人中心-历史记录",
            "goodshistorys":goodshistorys,
        }
        return render(request, "user_center_history.html", context=context)

class GoodsMatchColorUpload(View):
    """
    产品撞色信息上传
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
        goodss = Goods.objects.filter(b_brand=brand,g_time=time_t)
        gimgs = []
        for goods in goodss:
            goodsinfos = GoodsInformation.objects.filter(gi_goods=goods)
            for goodsinfo in goodsinfos:
                gimgs.append(GoodsImage.objects.filter(gimg_gi_goods=goodsinfo)[0])
        context = {
            "brand": brand,
            "brands": brands,
            "time_t": time_t,
            "times": times,
            "gimgs":gimgs,
            "title":"产品撞色信息上传"
        }
        return render(request,"goods_match_color_upload.html",context=context)

    def post(self,request):
        gi_ids = request.POST.getlist("gi_id")
        for gi_id in gi_ids:
            goodsinfo = GoodsInformation.objects.get(pk=gi_id)
            goodsinfo.gi_match_color = True
            goodsinfo.save()
        return HttpResponse("ok")