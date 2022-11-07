from io import BytesIO

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django import forms

from app01 import models
from app01.utils.code import check_code
from app01.utils.pagination import Pageination

import ScrapyBilibili


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="姓名")
    code = forms.CharField(
        label="验证码",
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control"}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")
        return pwd


def index(request):
    """用户界面"""
    data_list = models.UserInfo.objects.all()
    page_object = Pageination(request, data_list, page_size=10)
    # ScrapyBilibili.get_peoson(36676936)
    context = {
        "data": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    # user = models.UserInfo.objects.filter(id=19).first()
    # print(user)
    # user.password = '123456789'
    # user.save()
    # print("success")
    return render(request, "index.html", context)


def add_user(request):
    """添加用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "adduser.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 若数据合法
        print(form.cleaned_data)
        form.save()
        return redirect("/index/")
    # 校验失败,这里的form包含原来的数据，与错误信息
    return render(request, "adduser.html", {"form": form})


def edit_user(request, nid):
    """编辑用户"""
    # 从数据库里获取想要的那一行数据（对象）
    obj = models.UserInfo.objects.filter(id=nid).first()
    if obj is None:
        pass  # 返回一个错误页面

    if request.method == "GET":
        form = UserModelForm(instance=obj)
        return render(request, "edituser.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/index/")
    # 校验失败,这里的form包含原来的数据，与错误信息
    return render(request, "edituser.html", {"form": form})


def delete_user(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/index/")


def image_code(request):
    img, code_string = check_code()
    print(code_string)

    stream = BytesIO()
    img.save(stream, 'png')

    # 写入到自己的session
    request.session["image_code"] = code_string
    # 给Session超时时间 180秒
    request.session.set_expiry(180)

    return HttpResponse(stream.getvalue())
