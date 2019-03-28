from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.base import View
from .models import *
from django.core.paginator import Paginator
from goods.goods_query_view import *
from django.db.models import Q
from goods_info.settings import BASE_DIR
from goods.update_goods_data import *
import uuid
import json
import os
import datetime

def date_str(date):
    """
    转换时间格式
    :param date:
    :return:
    """
    return str(date.replace("年","-").replace("月","-").replace("日",""))

def date_conversion(time_d):
    """
    将时间目录转化为时间
    :param time_dir:
    :return:
    """
    time_dir = [int(i) for i in time_d.split("-")]
    brand_time = datetime.date(time_dir[0], time_dir[1], time_dir[2])
    return brand_time

class GoodsChange(View):
    def get(self,request):
        """
        变化数据确认
        :param request:
        :return:
        """
        brands = Brand.objects.filter()
        price_changes = []
        extence_changes = []
        order_changes = []
        color_changes = []
        for brand in brands:
            brandtimes = BrandTime.objects.filter(bt_brand=brand)
            price_times = []
            extence_times = []
            order_times = []
            color_times = []
            if len(brandtimes) > 1:
                for bt_index in range(1,len(brandtimes)):
                    now_time = brandtimes[bt_index].bt_time
                    before_time = brandtimes[bt_index-1].bt_time
                    #价格
                    pacs_price = ProductAnalysisConfirmation.objects.filter(pac_brand=brand.b_name,
                                                                            pac_type="price",
                                                                            pac_now_time=now_time,
                                                                            pac_before_time=before_time)
                    if len(pacs_price) == 0:
                        price_times.append({
                            "now_time":now_time,
                            "before_time":before_time,
                        })
                    #上下架
                    pacs_extence = ProductAnalysisConfirmation.objects.filter(pac_brand=brand.b_name,
                                                                            pac_type="extence",
                                                                            pac_now_time=now_time,
                                                                            pac_before_time=before_time)
                    if len(pacs_extence) == 0:
                        extence_times.append({
                            "now_time": now_time,
                            "before_time": before_time,
                        })
                    # 位置
                    pacs_order = ProductAnalysisConfirmation.objects.filter(pac_brand=brand.b_name,
                                                                            pac_type="order",
                                                                            pac_now_time=now_time,
                                                                            pac_before_time=before_time)
                    if len(pacs_order) == 0:
                        order_times.append({
                            "now_time": now_time,
                            "before_time": before_time,
                        })
                    # 颜色
                    pacs_color = ProductAnalysisConfirmation.objects.filter(pac_brand=brand.b_name,
                                                                            pac_type="color",
                                                                            pac_now_time=now_time,
                                                                            pac_before_time=before_time)
                    if len(pacs_color) == 0:
                        color_times.append({
                            "now_time": now_time,
                            "before_time": before_time,
                        })

                price_changes.append({
                    "brand":brand,
                    "type":"price",
                    "price_times":price_times,
                })
                extence_changes.append({
                    "brand":brand,
                    "type":"extence",
                    "extence_times":extence_times,
                })
                order_changes.append({
                    "brand":brand,
                    "type":"order",
                    "order_times":order_times,
                })
                color_changes.append({
                    "brand":brand,
                    "type":"color",
                    "color_times":color_times,
                })
        context = {
            "price_changes":price_changes,
            "extence_changes":extence_changes,
            "order_changes":order_changes,
            "color_changes":color_changes,
        }
        return render(request,"goods_change_data.html",context=context)

    def post(self,request):
        type = request.POST.get("type")
        brand_timeslist = request.POST.getlist("brand_times")
        timeslist = [i.split(":")[1] for i in brand_timeslist]
        brandlist = [i.split(":")[0] for i in brand_timeslist]
        func = getattr(self,type)
        func(timeslist,brandlist)
        return HttpResponse("ok")

    def price(self,timelist,brandlist):
        """
        价格变动
        :param timelist:
        :param brandlist:
        :return:
        """
        for tb_index in range(len(timelist)):
            #处理价格变动数据
            b_name = brandlist[tb_index]
            brand = Brand.objects.get(b_name=b_name)
            times = [date_conversion(date_str(i)) for i in timelist[tb_index].split("&")]
            now_time = Time.objects.get(t_time=times[0])
            previous_time = Time.objects.get(t_time=times[1])
            #单个品牌商所有产品的名字
            goods_names = self._goods_name(brand)
            price_change_infos = []
            for goods_name in goods_names:
                now_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=now_time)
                previous_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=previous_time)
                if len(now_goods) != 0 and len(previous_goods) != 0:
                    now_price = now_goods[0].g_now_price #本期价格
                    previous_price = previous_goods[0].g_now_price #上期价格
                    price_type = now_goods[0].g_price_type #价格类型
                    price_change = float(now_price) - float(previous_price) #价格变化
                    #价格变化状态
                    price_state = 0
                    if price_change == 0:
                        price_state = 0
                    elif price_change > 0:
                        price_state = 1
                    elif price_change < 0:
                        price_state = 2

                    if price_state != 0:  # 只有状态变化的产品才存入
                        price_change_infos.append({
                            "price_type":price_type,
                            "previous_price":previous_price,
                            "now_price":now_price,
                            "price_change":price_change,
                            "price_state":price_state,
                            "previous_goods":previous_goods[0],
                            "now_goods":now_goods[0],
                            "time":now_time,
                        })
            data = {
                "brand":brand,
                "price_change_infos":price_change_infos,
                "times":times,
            }
            #价格变化入库
            self._price_change(data)

    def _price_change(self,data):
        """
        产品价格变化入库
        :param data:
        :return:
        """
        print("%s的产品价格变化开始入库！"%data["brand"].b_name)
        for price_change_info in data["price_change_infos"]:
            gpc = GoodsPriceChange()
            gpc.gpc_id = str(uuid.uuid1())
            gpc.gpc_price_type = price_change_info["price_type"]
            gpc.gpc_previous_price = price_change_info["previous_price"]
            gpc.gpc_now_price = price_change_info["now_price"]
            gpc.gpc_price_change = price_change_info["price_change"]
            gpc.gpc_price_state = price_change_info["price_state"]
            gpc.gpc_previous_goods = price_change_info["previous_goods"]
            gpc.gpc_now_goods = price_change_info["now_goods"]
            gpc.gpc_time = price_change_info["time"]
            gpc.save()
            print("%s的变化上传完毕！"%price_change_info["now_goods"].g_name)

        pac = {
            "b_name":data["brand"].b_name,
            "type":"price",
            "before_time":data["times"][1],
            "now_time":data["times"][0],
        }
        self._goods_pac(pac)

    def extence(self,timelist,brandlist):
        """
        上下架变化
        :param timelist:
        :param brandlist:
        :return:
        """
        for tb_index in range(len(timelist)):
            #处理上下架变动数据
            b_name = brandlist[tb_index]
            brand = Brand.objects.get(b_name=b_name)
            times = [date_conversion(date_str(i)) for i in timelist[tb_index].split("&")]
            now_time = Time.objects.get(t_time=times[0])
            previous_time = Time.objects.get(t_time=times[1])
            #单个品牌商所有产品的名字
            goods_names = self._goods_name(brand)
            goods_extence_infos = []
            for goods_name in goods_names:
                now_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=now_time)
                previous_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=previous_time)
                #上架
                if len(now_goods) != 0 and len(previous_goods) == 0:
                    goods_extence_infos.append({
                        "extence_type":2,
                        "extence_goods":now_goods[0],
                        "extence_now_time":now_time.t_time,
                        "extence_before_time":previous_time.t_time,
                    })
                elif len(now_goods) == 0 and len(previous_goods) != 0:
                    goods_extence_infos.append({
                        "extence_type": 1,
                        "extence_goods": previous_goods[0],
                        "extence_now_time":now_time.t_time,
                        "extence_before_time":previous_time.t_time,
                    })

            data = {
                "brand": brand,
                "goods_extence_infos": goods_extence_infos,
                "times": times,
            }
            # print(data)
            self._extence_change(data)

    def _extence_change(self,data):
        """
        上下架入库
        :param data:
        :return:
        """
        print("%s的产品上下架变化开始入库！" % data["brand"].b_name)
        for goods_extence_info in data["goods_extence_infos"]:
            gec = GoodsExtenceChange()
            gec.gec_id = str(uuid.uuid1())
            gec.gec_extence_type = goods_extence_info["extence_type"]
            gec.gec_extence_goods = goods_extence_info["extence_goods"]
            gec.gec_extence_now_time = goods_extence_info["extence_now_time"]
            gec.gec_extence_before_time = goods_extence_info["extence_before_time"]
            gec.save()
            print("%s的变化上传完毕！" % goods_extence_info["extence_goods"].g_name)

        pac = {
            "b_name": data["brand"].b_name,
            "type": "extence",
            "before_time": data["times"][1],
            "now_time": data["times"][0],
        }
        self._goods_pac(pac)

    def order(self, timelist, brandlist):
        """
        网站位置变化
        :param timelist:
        :param brandlist:
        :return:
        """
        for tb_index in range(len(timelist)):
            #处理位置变动数据
            b_name = brandlist[tb_index]
            brand = Brand.objects.get(b_name=b_name)
            times = [date_conversion(date_str(i)) for i in timelist[tb_index].split("&")]
            now_time = Time.objects.get(t_time=times[0])
            previous_time = Time.objects.get(t_time=times[1])
            #单个品牌商所有产品的名字
            goods_names = self._goods_name(brand)
            goods_order_infos = []
            for goods_name in goods_names:
                now_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=now_time)
                previous_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=previous_time)
                if len(now_goods) != 0 and len(previous_goods) != 0:
                    now_goods_infos = GoodsInformation.objects.filter(gi_goods=now_goods[0])
                    previous_goods_infos = GoodsInformation.objects.filter(gi_goods=previous_goods[0])
                    now_goods_informations = [[i.gi_color,i.gi_model,i.gi_gender,i.gi_page,] for i in now_goods_infos]
                    previous_goods_informations = [[i.gi_color,i.gi_model,i.gi_gender,i.gi_page,] for i in previous_goods_infos]
                    goods_order_change_changes = []
                    if len(now_goods_infos) >= len(previous_goods_infos):
                        for now_goods_information in now_goods_informations:
                            if now_goods_information in previous_goods_informations:
                                now_index = now_goods_informations.index(now_goods_information) #本期产品位置的列表下标
                                previous_index = previous_goods_informations.index(now_goods_information) #上期产品位置的列表下标
                                now_info = now_goods_infos[now_index]
                                previous_info = previous_goods_infos[previous_index]
                                previous_order = previous_info.gi_order #上期位置
                                now_order = now_info.gi_order #本期位置
                                # print(goods_name,previous_order,now_order)
                                order_change = int(previous_order) - int(now_order) #位置变化
                                # 产品位置变化状态
                                order_state = 0
                                if order_change == 0:
                                    order_state = 0
                                elif order_change > 0:
                                    order_state = 1
                                elif order_change < 0:
                                    order_state = 2
                                if order_change != 0:
                                    goods_order_change_changes.append({
                                        "now_goods_id":now_info.gi_id,
                                        "previous_order":previous_order,
                                        "now_order":now_order,
                                        "order_change":order_change,
                                        "order_state":order_state,
                                        "sex":now_info.gi_gender,
                                        "page":now_info.gi_page,
                                    })
                    elif len(now_goods_infos) < len(previous_goods_infos):
                        for previous_goods_information in previous_goods_informations:
                            if previous_goods_information in now_goods_informations:
                                now_index = now_goods_informations.index(previous_goods_information) #本期产品位置的列表下标
                                previous_index = previous_goods_informations.index(previous_goods_information) #上期产品位置的列表下标
                                now_info = now_goods_infos[now_index]
                                previous_info = previous_goods_infos[previous_index]
                                previous_order = previous_info.gi_order #上期位置
                                now_order = now_info.gi_order #本期位置
                                order_change = int(previous_order) - int(now_order) #位置变化
                                # print(goods_name, previous_order, now_order)
                                # 产品位置变化状态
                                order_state = 0
                                if order_change == 0:
                                    order_state = 0
                                elif order_change > 0:
                                    order_state = 1
                                elif order_change < 0:
                                    order_state = 2
                                if order_change != 0:
                                    goods_order_change_changes.append({
                                        "now_goods_id":now_info.gi_id,
                                        "previous_order":previous_order,
                                        "now_order":now_order,
                                        "order_change":order_change,
                                        "order_state":order_state,
                                        "sex": now_info.gi_gender,
                                        "page":now_info.gi_page,
                                    })

                    goods_order_infos.append({
                        "previous_goods":previous_goods[0],
                        "now_goods":now_goods[0],
                        "now_time":now_time.t_time,
                        "before_time":previous_time.t_time,
                        "goods_order_change_changes":goods_order_change_changes,
                    })

            data = {
                "brand": brand,
                "goods_order_infos": goods_order_infos,
                "times": times,
            }
            self._order_change(data)

    def _order_change(self,data):
        """
        位置变化上传
        :param data:
        :return:
        """
        print("%s的产品位置变化开始入库！" % data["brand"].b_name)
        for goods_order_info in data["goods_order_infos"]:
            goc_id = str(uuid.uuid1())
            goc = GoodsOrderChange()
            goc.goc_id = goc_id
            goc.goc_previous_goods = goods_order_info["previous_goods"]
            goc.goc_now_goods = goods_order_info["now_goods"]
            goc.goc_now_time = goods_order_info["now_time"]
            goc.goc_before_time = goods_order_info["before_time"]
            goc.save()
            goods_goc = GoodsOrderChange.objects.get(goc_id=goc_id)
            for goods_order_change_change in goods_order_info["goods_order_change_changes"]:
                gocc = GoodsOrderChangeChange()
                gocc.gocc_id = str(uuid.uuid1())
                gocc.gocc_now_goods_id = goods_order_change_change["now_goods_id"]
                gocc.gocc_previous_order = goods_order_change_change["previous_order"]
                gocc.gocc_now_order = goods_order_change_change["now_order"]
                gocc.gocc_order_change = goods_order_change_change["order_change"]
                gocc.gocc_order_state = goods_order_change_change["order_state"]
                gocc.gocc_sex = goods_order_change_change["sex"]
                gocc.gocc_page = goods_order_change_change["page"]
                gocc.goocc_goc = goods_goc
                gocc.save()
            print("%s的变化上传完毕！" % goods_order_info["now_goods"].g_name)
        pac = {
            "b_name": data["brand"].b_name,
            "type": "order",
            "before_time": data["times"][1],
            "now_time": data["times"][0],
        }
        self._goods_pac(pac)

    def color(self, timelist, brandlist):
        """
        颜色变化
        :return:
        """
        for tb_index in range(len(timelist)):
            #处理颜色变动数据
            b_name = brandlist[tb_index]
            brand = Brand.objects.get(b_name=b_name)
            times = [date_conversion(date_str(i)) for i in timelist[tb_index].split("&")]
            now_time = Time.objects.get(t_time=times[0])
            previous_time = Time.objects.get(t_time=times[1])
            #单个品牌商所有产品的名字
            goods_names = self._goods_name(brand)
            goods_color_infos = []
            for goods_name in goods_names:
                now_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=now_time)
                previous_goods = Goods.objects.filter(g_name=goods_name,b_brand=brand,g_time=previous_time)
                if len(now_goods) != 0 and len(previous_goods) != 0:
                    now_goods_infos = GoodsInformation.objects.filter(gi_goods=now_goods[0])
                    previous_goods_infos = GoodsInformation.objects.filter(gi_goods=previous_goods[0])
                    now_goods_colors = [i.gi_color for i in now_goods_infos]
                    previous_goods_colors = [i.gi_color for i in previous_goods_infos]
                    up_color_infos = []
                    down_color_infos = []
                    #颜色上架
                    for now_goods_color in now_goods_colors:
                        if now_goods_color not in previous_goods_colors:
                            up_color_index = now_goods_colors.index(now_goods_color)
                            up_color_infos.append(now_goods_infos[up_color_index])
                    #颜色下架
                    for previous_goods_color in previous_goods_colors:
                        if previous_goods_color not in now_goods_colors:
                            down_color_index = previous_goods_colors.index(previous_goods_color)
                            down_color_infos.append(previous_goods_infos[down_color_index])
                    #上架
                    if len(up_color_infos) != 0:
                        goods_color_infos.append({
                            "change_color_num": len(up_color_infos),  # 颜色变化数量
                            "change_color_state": 1,  # 颜色变化类型
                            "previous_goods": previous_goods[0],  # 上一次产品
                            "now_goods": now_goods[0],  # 当前产品
                            "time": now_time.t_time,  # 当前时间
                            "the_shelves_colors": up_color_infos,  # 产品变化颜色
                        })
                    #下架
                    if len(down_color_infos) != 0:
                        goods_color_infos.append({
                            "change_color_num": len(down_color_infos),  # 颜色变化数量
                            "change_color_state": 2,  # 颜色变化类型
                            "previous_goods": previous_goods[0],  # 上一次产品
                            "now_goods": now_goods[0],  # 当前产品
                            "time": now_time.t_time,  # 当前时间
                            "the_shelves_colors": down_color_infos,  # 产品变化颜色
                        })
            data = {
                "brand": brand,
                "goods_color_infos": goods_color_infos,
                "times": times,
            }
            self._color_change(data)


    def _color_change(self,data):
        """
        产品颜色变化入库
        :param data:
        :return:
        """
        print("%s的产品颜色变化开始入库！" % data["brand"].b_name)
        for goods_color_info in data["goods_color_infos"]:
            gcc_id = str(uuid.uuid1())
            gcc = GoodsColorChange()
            gcc.gcc_id = gcc_id
            gcc.gcc_change_color_num = goods_color_info["change_color_num"]
            gcc.gcc_change_color_state = goods_color_info["change_color_state"]
            gcc.gcc_previous_goods = goods_color_info["previous_goods"]
            gcc.gcc_now_goods = goods_color_info["now_goods"]
            gcc.gcc_time = goods_color_info["time"]
            gcc.save()
            goods_gcc = GoodsColorChange.objects.get(gcc_id=gcc_id)
            for the_shelves_color in goods_color_info["the_shelves_colors"]:
                gccc = GoodsColorChangeColor()
                gccc.gccc_id = str(uuid.uuid1())
                gccc.gccc_color = the_shelves_color.gi_color
                gccc.gccc_goodscolorchange = goods_gcc
                gccc.save()
            print("%s的变化上传完毕！" % goods_color_info["now_goods"].g_name)
        pac = {
            "b_name": data["brand"].b_name,
            "type": "color",
            "before_time": data["times"][1],
            "now_time": data["times"][0],
        }
        self._goods_pac(pac)


    def _goods_pac(self,data):
        """
        产品分析上传确认
        :param pac:
        :return:
        """
        pac = ProductAnalysisConfirmation()
        pac.pac_id = str(uuid.uuid1())
        pac.pac_brand = data["b_name"]
        pac.pac_type = data["type"]
        pac.pac_before_time = data["before_time"]
        pac.pac_now_time = data["now_time"]
        pac.save()

    def _goods_name(self,brand):
        """
        单个品牌商所有产品的名字
        :param brand:
        :return:
        """
        goodss = Goods.objects.filter(b_brand=brand)
        goods_names = list(set([i.g_name for i in goodss]))
        return goods_names