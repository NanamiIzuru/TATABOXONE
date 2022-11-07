import time
import csv

from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from app01 import models

import ScrapyBilibili


def people(request):
    #
    uid = request.GET.get('uid', "")
    if uid:
        uid = int(uid)
        if uid <= 0:
            return render(request, "people.html")
        flag = models.PeopleInfo.objects.filter(mid=uid).exists()
        if flag:
            print("people: 用户存在！")
        else:
            print("people: 不存在！需要爬取")
            ScrapyBilibili.get_video(uid)
        # 爬取到数据之后
        people_info = models.PeopleInfo.objects.filter(mid=uid).first()
        # 视频分区信息在这里查看
        typelist = {}
        video_info = models.VideoInfo.objects.filter(owner_mid=uid)
        if people_info.count > 0:
            for i in video_info:
                if typelist.get(i.type_name):
                    typelist[i.type_name]['count'] += 1
                else:
                    typelist[i.type_name] = {'id': i.type_id, 'count': 1}

        typeid = int(request.GET.get('typeid', "0"))
        sort = request.GET.get('sort', "")
        sort_type = ['view', 'like', 'coin', 'favourite', 'share']
        data = {
            'owner_mid': uid,
        }
        if typeid:
            data['type_id'] = typeid
        if sort in sort_type:
            video_info = models.VideoInfo.objects.filter(**data).order_by("-"+sort)
        else:
            video_info = models.VideoInfo.objects.filter(**data)
        dic = {
            'people': people_info,
            'count': people_info.count,
            'video': video_info,
            'typelist': typelist,
            'sort': sort,
            'choice': typeid,
        }
        return render(request, "people.html", dic)

    return render(request, "people.html")


def people_search(request):
    # 把获取到的uid转成整形
    uid = request.GET.get('uid')
    dic = {
        'status': False,
    }
    try:
        uid = int(uid)
        if uid > 0:
            print(uid)
            result = models.PeopleInfo.objects.filter(mid=uid).exists()
            if not result:
                print("search：找不到用户信息！需要爬取！")
                ScrapyBilibili.get_video(uid)
                dic['status'] = True
            else:
                print("search：找到用户！")
                dic['status'] = True
            dic['uid'] = uid
    finally:
        pass
    return JsonResponse(dic)


def reload_video(request):
    dic = {
        'status': False,
    }
    try:
        uid = request.GET.get('uid', '')
        if uid:
            uid = int(uid)
            if uid > 0:
                uid = int(uid)
                ScrapyBilibili.get_video(uid)
                dic['uid'] = uid
                dic['status'] = True
                return JsonResponse(dic)
    finally:
        pass
    return JsonResponse(dic)


def people_save(request):
    uid = request.GET.get('uid')
    try:
        assert int(uid) > 0
    except:
        return HttpResponse("uid格式不正确！")
    uid = int(uid)
    data = models.VideoInfo.objects.filter(owner_mid=uid)
    info = []
    for i in data:
        dic = i.__dict__
        dic.pop('_state')
        info.append(dic)
    headers = list(info[0].keys())
    t = str(int(time.time()))
    n = models.PeopleInfo.objects.filter(mid=uid).first().name
    name = n + '_' + t +'.csv'
    place = 'tempdatas/' + name
    print(place)
    print(type(place))
    with open(place, 'w', newline='', encoding='utf-8') as f:
        c = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
        c.writeheader()
        for i in info:
            c.writerow(i)
    response = FileResponse(open(place, 'rb'))
    response['COntent-Disposotion'] = 'attachment;filename=' + name
    return response
