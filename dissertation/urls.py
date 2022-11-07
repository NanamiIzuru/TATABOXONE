"""dissertation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01 import views
from app01.myView import user, pretty, popular, people

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', user.index),
    # 用户
    path('adduser/', user.add_user),
    path('edituser/<int:nid>/', user.edit_user),
    path('delete/<int:nid>/', user.delete_user),
    path('img/code/', user.image_code),
    # 靓号
    path('prettylist/', pretty.pretty_list),
    path('prettyadd/', pretty.pretty_add),
    path('prettyedit/<int:nid>/', pretty.pretty_edit),
    path('prettydelete/<int:nid>/', pretty.pretty_delete),

    # 热门视频信息
    path('popular/', popular.popular),
    path('popular/reload/', popular.popular_reload),
    path('popular/save/', popular.popular_save),
    # 用户信息
    path('people/', people.people),
    path('people/search/', people.people_search),
    path('people/reload/', people.reload_video),
    path('people/save/', people.people_save),
]
