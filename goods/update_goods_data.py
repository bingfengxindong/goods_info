from goods.models import *
from goods_info.settings import BASE_DIR
from lxml import etree
from retrying import retry
import csv
import datetime
import uuid
import requests
import os
import time
import random


header = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "upgrade-insecure-requests":"1",
}

def date_conversion(time_d):
    """
    将时间目录转化为时间
    :param time_dir:
    :return:
    """
    time_dir = [int(i) for i in time_d.split("-")]
    brand_time = datetime.date(time_dir[0], time_dir[1], time_dir[2])
    return brand_time

class UpdateGoodsDate:
    """
    上传产品数据
    """
    def __init__(self,brand_path):
        self.brand_path = brand_path
        self.main()

    def main(self):
        brand_datas = self._readdata()
        goods_infos = self._data_process(brand_datas)
        brand_infos = self._data_heavy(goods_infos)
        self._brand_info_storage(brand_infos)

    def _readdata(self):
        """
        读取数据
        :return:
        """
        file_data = csv.reader(open(self.brand_path,"r",encoding="utf-8"))
        brand_name = self.brand_path.split("\\")[-1].split(".")[0]
        upload_time = self.brand_path.split("\\")[-2]
        datas = [i for i in file_data if i != []]
        return {
            "brand_name":brand_name,
            "upload_time":upload_time,
            "datas":datas,
        }

    def _data_process(self,datas):
        """
        数据处理
        :param datas:
        :return:
        """
        global goods_page
        global goods_url
        upload_time = datas["upload_time"]
        brand_name = datas["brand_name"]
        brand_datas = datas["datas"]
        brand_titles = brand_datas[0]
        brand_infos = brand_datas[1:]
        goods_infos = []
        for brand_info in brand_infos:
            name_index = self._data_judge("goods_name",brand_titles)
            model_index = self._data_judge("goods_model",brand_titles)
            price_index = self._data_judge("goods_price",brand_titles)
            discount_price_index = self._data_judge("goods_discount_price",brand_titles)
            color_index = self._data_judge("goods_color",brand_titles)
            size_index = self._data_judge("goods_size",brand_titles)
            details_index = self._data_judge("goods_details",brand_titles)
            images_index = self._data_judge("goods_images",brand_titles)
            title_index = self._data_judge("goods_title",brand_titles)
            order_index = self._data_judge("goods_num",brand_titles)
            gender_index = self._data_judge("gender",brand_titles)
            page_index = self._data_judge("goods_page",brand_titles)
            comments_index = self._data_judge("goods_comments",brand_titles)
            goods_url_index = self._data_judge("goods_url",brand_titles)
            goods_type_index = self._data_judge("goods_type",brand_titles)
            # print(brand_name)
            # print(brand_info[price_index])
            if name_index != None:
                goods_name = brand_info[name_index]
            if model_index != None:
                goods_model = brand_info[model_index]
            if price_index != None:
                goods_price_type = brand_info[price_index][0]
                goods_price = brand_info[price_index]
            if discount_price_index != None:
                goods_discount_price = brand_info[discount_price_index]
            if color_index != None:
                goods_color = brand_info[color_index]
            if size_index != None:
                goods_sizes = brand_info[size_index]
            if details_index != None:
                goods_details = brand_info[details_index]
            if images_index != None:
                goods_images = brand_info[images_index]
            if title_index != None:
                goods_title = brand_info[title_index]
            else:
                goods_title = ""
            if order_index != None:
                goods_order = brand_info[order_index]
            if gender_index != None:
                goods_gender = brand_info[gender_index]
            if page_index != None:
                goods_page = brand_info[page_index]
            if comments_index != None:
                goods_comments = brand_info[comments_index]
            else:
                goods_comments = ""
            if goods_url_index != None:
                goods_url = brand_info[goods_url_index]
            if goods_type_index != None:
                goods_type = brand_info[goods_type_index]
            goods_infos.append({
                "goods_name":goods_name,
                "goods_model":goods_model,
                "goods_price_type":goods_price_type,
                "goods_price":goods_price,
                "goods_discount_price":goods_discount_price,
                "goods_color":goods_color,
                "goods_sizes":goods_sizes,
                "goods_details":goods_details,
                "goods_images":goods_images,
                "goods_title":goods_title,
                "goods_order":goods_order,
                "goods_gender":goods_gender,
                "goods_page":goods_page,
                "goods_comments":goods_comments,
                "goods_url":goods_url,
                "goods_type":goods_type,
            })
        return {
            "brand_name":brand_name,
            "upload_time":upload_time,
            "goods_infos":goods_infos,
        }

    def _data_heavy(self,goods_infos):
        """
        数据去重
        :param goods_infos:
        :return:
        """
        brand_name = goods_infos["brand_name"]
        upload_time = goods_infos["upload_time"]
        goods_infos = goods_infos["goods_infos"]
        goods_heavy_infos = self._goods_info_heavy(goods_infos)
        brand_goodss = []
        for goods_heavy_info in goods_heavy_infos:
            goods_name = [i["goods_name"] for i in goods_heavy_info][0]
            goods_model = [i["goods_model"] for i in goods_heavy_info]
            goods_price_type = [i["goods_price_type"] for i in goods_heavy_info][0]
            goods_now_price = [i["goods_price"] for i in goods_heavy_info][0]
            goods_discount_price = [i["goods_discount_price"] for i in goods_heavy_info][0]
            goods_color = [i["goods_color"] for i in goods_heavy_info]
            goods_sizes = [i["goods_sizes"] for i in goods_heavy_info]
            goods_details = [i["goods_details"] for i in goods_heavy_info]
            goods_images = [i["goods_images"] for i in goods_heavy_info]
            goods_title = [i["goods_title"] for i in goods_heavy_info][0]
            goods_order = [i["goods_order"] for i in goods_heavy_info]
            goods_gender = [i["goods_gender"] for i in goods_heavy_info]
            goods_page = [i["goods_page"] for i in goods_heavy_info]
            goods_comments = [i["goods_comments"] for i in goods_heavy_info][0]
            goods_urls = [i["goods_url"] for i in goods_heavy_info]
            goods_types = [i["goods_type"] for i in goods_heavy_info][0]
            goods_informations = []
            for data_index in range(len(goods_model)):
                goods_informations.append({
                    "goods_url":goods_urls[data_index],
                    "goods_model":goods_model[data_index],
                    "goods_color":goods_color[data_index],
                    "goods_order":goods_order[data_index],
                    "goods_gender":goods_gender[data_index],
                    "goods_page":goods_page[data_index],
                    "goods_sizes":goods_sizes[data_index],
                    "goods_details":goods_details[data_index],
                    "goods_images":goods_images[data_index],
                })
            brand_goodss.append({
                "goods_name":goods_name,
                "goods_title":goods_title,
                "goods_price_type":goods_price_type,
                "goods_discount_price":goods_discount_price,
                "goods_now_price":goods_now_price,
                "goods_comments":goods_comments,
                "goods_informations":goods_informations,
                "goods_type": goods_types,
            })
        return {
            "brand_name":brand_name,
            "upload_time":upload_time,
            "brand_goodss":brand_goodss,
        }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def _brand_info_storage(self,brand_infos):
        """
        产品信息存入数据库
        :param brand_infos:
        :return:
        """
        brand_name = brand_infos["brand_name"]
        upload_time = brand_infos["upload_time"]
        print("品牌--%s"%brand_name)
        print("时间--%s"%upload_time)
        brand_time = date_conversion(upload_time)
        brands = Brand.objects.filter(b_name=brand_name)
        #确认品牌是否上传
        if len(brands) == 0:
            b_id = str(uuid.uuid1())
            b_bt = BrandType.objects.filter()[0]
            b = Brand()
            b.b_id = b_id
            b.b_name = brand_name
            b.b_bt = b_bt
            b.save()
            brand = Brand.objects.get(b_id=b_id)
            print("该品牌信息未上传！")
        else:
            brand = brands[0]
            print("该品牌信息已经上传！")
        brandtimes = BrandTime.objects.filter(bt_time=brand_time,bt_brand=brand)
        if len(brandtimes) == 0:
            bt_id = str(uuid.uuid1())
            bt = BrandTime()
            bt.bt_id = bt_id
            bt.bt_time = brand_time
            bt.bt_brand = brand
            bt.save()
            print("该品牌抓取时间的数据未上传！")
        else:
            print("该品牌抓取时间的数据已经上传！")

        #确认商品上传
        times = Time.objects.filter(t_time=brand_time)
        if len(times) == 1:
            g_time = times[0]
            print("该数据时间已经创建！")
        else:
            t_id = str(uuid.uuid1())
            t = Time()
            t.t_id = t_id
            t.t_time = brand_time
            t.save()
            g_time = Time.objects.get(t_id=t_id)

        brand_goodss = brand_infos["brand_goodss"]
        print(brand_infos["brand_goodss"])
        for brand_goods in brand_goodss:
            print("开始上传%s"%brand_goods["goods_name"])
            g_id = str(uuid.uuid1())
            g_type = GoodsType.objects.get(gt_type="未分类")
            g = Goods()
            g.g_id = g_id
            g.g_name = brand_goods["goods_name"]
            g.g_title = brand_goods["goods_title"]
            g.g_price_type = brand_goods["goods_price_type"]
            g.g_discount_price = brand_goods["goods_discount_price"].strip(brand_goods["goods_price_type"])
            g.g_now_price = brand_goods["goods_now_price"].strip(brand_goods["goods_price_type"])
            g.g_time = g_time
            g.b_brand = brand
            g.g_type = g_type
            g.g_goods_type = brand_goods["goods_type"]
            g.save()

            goods = Goods.objects.get(g_id=g_id)
            print("开始上传%s的产品评论"%brand_goods["goods_name"])
            goodscomments = brand_goods["goods_comments"]
            if goodscomments != "":
                if goodscomments != "none":
                    goodscomments = eval(goodscomments)
                    for goodscomment in goodscomments:
                        gc = GoodsComment()
                        gc.gc_id = str(uuid.uuid1())
                        if "/" in goodscomment["goods_comment_time"]:
                            comment_time = goodscomment["goods_comment_time"].split("/")
                        elif "-" in goodscomment["goods_comment_time"]:
                            comment_time = goodscomment["goods_comment_time"].split("-")
                        goods_comment_time = datetime.date(int(comment_time[0]),int(comment_time[1]),int(comment_time[2]))
                        gc.gc_comment_time = goods_comment_time
                        try:
                            gc.gc_comment = goodscomment["goods_comment_comment"]
                        except:
                            gc.gc_comment = "goods"
                        gc.gc_comment_star = int(goodscomment["goods_comment_star"])
                        gc.gc_goods = goods
                        gc.save()

            print("开始上传%s的产品信息"%brand_goods["goods_name"])
            goods_informations = brand_goods["goods_informations"]
            for goods_information in goods_informations:
                gi_id = str(uuid.uuid1())
                gi_color_type = GoodsColorType.objects.get(gct_color_type="未分类")
                gi = GoodsInformation()
                gi.gi_id = gi_id
                gi.gi_model = goods_information["goods_model"]
                gi.gi_color = goods_information["goods_color"]
                gi.gi_order = int(goods_information["goods_order"])
                gi.gi_gender = goods_information["goods_gender"]
                gi.gi_brand_goods_url = goods_information["goods_url"]
                gi.gi_page = int(goods_information["goods_page"])
                gi.gi_goods = goods
                gi.gi_color_type = gi_color_type
                gi.save()

                goodsinformation = GoodsInformation.objects.get(gi_id=gi_id)
                print("开始上传%s的尺寸"%brand_goods["goods_name"])
                goodssizes = eval(goods_information["goods_sizes"])
                for goodssize in goodssizes:
                    gs = GoodsSize()
                    gs.gs_id = str(uuid.uuid1())
                    gs.gs_size = goodssize
                    gs.gs_gi = goodsinformation
                    gs.save()

                print("开始上传%s的详情"%brand_goods["goods_name"])
                goods_details = eval(goods_information["goods_details"])
                for goods_detail in goods_details:
                    gd = GoodsDetail()
                    gd.gd_id = str(uuid.uuid1())
                    gd.gd_detail = goods_detail
                    gd.gd_gi = goodsinformation
                    gd.save()

                print("开始上传%s的图片-----%.2f%%"%(brand_goods["goods_name"],(goods_informations.index(goods_information) + 1)/len(goods_informations) * 100))
                goods_image_dir = os.path.join(BASE_DIR, "static", "media", "image", upload_time, brand_name)
                isExists = os.path.exists(goods_image_dir)
                if not isExists: #判断是否存在目录
                    os.makedirs(goods_image_dir)
                if brand_name == "monki":
                    goods_images = goods_information["goods_images"].strip("['").strip("']").split("', '")
                    print(goods_images)
                else:
                    goods_images = eval(goods_information["goods_images"])
                for goods_image in goods_images:
                    print(brand_name,goods_image)
                    print("开始下载%s"%goods_image)

                    if brand_name == "nike":
                    #     图片下载
                        image_name = "%s.jpg" % goods_image.split("/")[-2]
                    elif brand_name == "hm" or brand_name == "kenzo" or brand_name == "prada":
                        image_name = "{}.jpg".format(uuid.uuid1())
                    else:
                        image_name = goods_image.split("/")[-1].split("?")[0]
                    try:
                        gimg = GoodsImage()
                        gimg.gimg_id = str(uuid.uuid1())
                        gimg.gimg_path = os.path.join("image",upload_time,brand_name,image_name)
                        gimg.gimg_url = goods_image
                        gimg.gimg_gi_goods = goodsinformation
                        gimg.save()

                        #图片下载
                        print(goods_image)
                        self._img_upload(goods_image,goods_image_dir,image_name)
                    except:
                        continue
            print("\033[1;31;47m",end="")
            print("%s上传完成-----%.2f%%"%(brand_goods["goods_name"],(brand_goodss.index(brand_goods) + 1)/len(brand_goodss) * 100),end="")
            print("\033[0m")

    @retry(stop_max_attempt_number=3)
    def _img_upload(self,goods_image,goods_image_dir,image_name):
        print(goods_image)
        response = requests.get(url=goods_image, headers=self.headers, timeout=10)
        image = response.content
        with open(os.path.join(goods_image_dir, image_name), "wb") as img:
            img.write(image)
        img.close()

    def _data_judge(self,data_field,field_list):
        """
        判断该数据是否存在
        :param data_field:
        :param field_list:
        :return:
        """
        if data_field in field_list:
            data_index = field_list.index(data_field)
        else:
            data_index = None
        return data_index

    def _goods_info_heavy(self,goods_infos):
        """
        产品信息去重
        :param goods_infos:
        :return:
        """
        goods_datas = []
        for data in goods_infos:
            g_data = []
            for i in goods_infos:
                if data["goods_name"] == i["goods_name"] and \
                        data["goods_price_type"] == i["goods_price_type"] and \
                        data["goods_title"] == i["goods_title"]:
                    g_data.append(i)
            if g_data not in goods_datas:
                goods_datas.append(g_data)
        return goods_datas