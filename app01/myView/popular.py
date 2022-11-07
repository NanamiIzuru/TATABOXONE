import time
import csv

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators import csrf

from app01 import models

import ScrapyBilibili


@csrf.csrf_exempt
def popular(request):
    query = models.PopularInfo.objects.all()
    # 分区计数
    type_name_list = {
        "国创": 0,
        "动画": 0,
        "鬼畜": 0,
        "舞蹈": 0,
        "娱乐": 0,
        "科技": 0,
        "美食": 0,
        "汽车": 0,
        "运动": 0,
        "游戏": 0,
        "音乐": 0,
        "影视": 0,
        "知识": 0,
        "资讯": 0,
        "生活": 0,
        "时尚": 0,
        "动物圈": 0,
    }
    for i in query:
        if i.type_name:
            type_name_list[i.type_name] += 1
    data = {}
    typeid = int(request.GET.get('typeid', "0"))
    sort = request.GET.get('sort', "")
    if typeid:
        data['type_id'] = typeid
    print(typeid)
    if sort == 'view':
        query = models.PopularInfo.objects.filter(**data).order_by("-view")
    elif sort == 'like':
        query = models.PopularInfo.objects.filter(**data).order_by("-like")
    elif sort == 'coin':
        query = models.PopularInfo.objects.filter(**data).order_by("-coin")
    elif sort == 'favourite':
        query = models.PopularInfo.objects.filter(**data).order_by("-favourite")
    elif sort == 'share':
        query = models.PopularInfo.objects.filter(**data).order_by("-share")
    else:
        query = models.PopularInfo.objects.filter(**data)

    current = {
        'typeid': typeid,
        'sort': sort,
        'query': query,
        'typelist': type_name_list
    }
    return render(request, "popular.html", current)


@csrf.csrf_exempt
def popular_reload(request):
    print("请求刷新页面！")
    dic = {'status': False}
    try:
        ScrapyBilibili.get_popular()
        dic['status'] = True
        return JsonResponse(dic)
    except BaseException as e:
        print(e)
    dic['status'] = False
    # time.sleep(5)
    # dic['status'] = True
    return JsonResponse(dic)


def popular_save(request):
    data = models.PopularInfo.objects.all()
    info = []
    for i in data:
        dic = i.__dict__
        dic.pop('_state')
        info.append(dic)
    headers = list(info[0].keys())
    t = str(int(time.time()))
    place = 'tempdatas/popular_' + t + '.csv'
    print(place)
    print(type(place))
    with open(place, 'w', newline='', encoding='utf-8') as f:
        c = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
        c.writeheader()
        for i in info:
            c.writerow(i)
    response = FileResponse(open(place, 'rb'))
    response['COntent-Disposotion'] = 'attachment;filename=' + t
    return response
