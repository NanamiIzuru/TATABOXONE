from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django import forms
from app01 import models
from app01.utils.pagination import Pageination


class PrettyModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    # mobile = forms.CharField(
    #     label="手机号码",
    #     validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误！')]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # exclude = ['level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        if len(mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号长度必须为11位！")
        flag = models.PrettyNum.objects.filter(mobile=mobile).exclude(id=self.instance.pk).exists()
        if not flag:
            # 通过则返回数据
            return mobile
        raise ValidationError("该号码已存在！")


def pretty_list(request):
    data = {}
    select_data = request.GET.get('q', "")
    if select_data:
        data["mobile__contains"] = select_data
    queryset = models.PrettyNum.objects.filter(**data).order_by("-level")
    page_object = Pageination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "selete_data": select_data,
        "page_string": page_object.html(),
        "page": page_object.page
    }
    return render(request, "prettylist.html", context)


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "prettyadd.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 若数据合法
        print(form.cleaned_data)
        form.save()
        return redirect("/prettylist/")
    return render(request, "prettyadd.html", {"form": form})


def pretty_edit(request, nid):
    obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyModelForm(instance=obj)
        return render(request, "prettyedit.html", {"form": form})

    form = PrettyModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/prettylist/')

    return render(request, "prettyedit.html", {"form": form})


def pretty_delete(request, nid):
    data = request.GET.get("page")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/prettylist/?page={}'.format(data))
