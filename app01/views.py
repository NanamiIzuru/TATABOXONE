from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse
from django.views.decorators import csrf
# from django.core.exceptions import ValidationError
# from django import forms
# from app01 import models
# from app01.utils.pagination import Pageination
# import ScrapyBilibili

# Create your views here.


def popular(request):
    # print(request.method)
    return render(request, "popular.html")


@csrf.csrf_exempt
def popular_a(request):
    print(request.POST)
    dic = {'status': True}
    return JsonResponse(dic)


