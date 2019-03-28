from goods.models import *

def goods_time_query(goodss,time_id):
    """
    产品时间查询清洗
    :param goodss:
    :return:
    """
    goods_times = sorted(list(set([i.g_time.t_time for i in goodss])),reverse=True)
    times = [Time.objects.get(t_time=i) for i in goods_times]
    if time_id == "":
        goods_now_time = Time.objects.filter(t_time=goods_times[0]).order_by("pk")[0]
    else:
        goods_now_time = Time.objects.filter(t_id=time_id)[0]

    return {"times":times,"goods_now_time":goods_now_time}

def query_ip(request):
    # 获取ip
    if "HTTP_X_FORWARDED_FOR" in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip