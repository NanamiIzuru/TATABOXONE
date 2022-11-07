from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
class M1(MiddlewareMixin):
    """中间件"""

    def process_request(self, request):
        # 排除不需要登录的界面
        if request.path_info == "/login/":
            return

        info_dict = request.session.get("info")
        if info_dict:
            pass
         # 没有登陆过
        #return HttpResponse("请登录！")
        # print("M1 进来了!")

    def process_response(self, request, response):
        # print("M1 出去了！")
        return response

