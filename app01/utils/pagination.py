from django.utils.safestring import mark_safe
import copy
"""
使用方法：
在视图函数中   
    1、根据需要取筛选数据对象
    queryset = models.PrettyNum.objects.filter(**data).order_by("-level")
    
    2、实例化分页对象
    page_object = Pageination(request, queryset)
    
    context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成分页html
        }
                
    3、在html中导入
    在html中
        {% for i in queryset %}
            <tr>
                <th scope="row">{{ i.id }}</th>
                <td>{{ i.mobile }}</td>
                <td>
                    <a class="btn btn-primary btn-xs" href="/prettyedit/{{ i.id }}/">编辑</a>
                    <a class="btn btn-danger btn-xs" href="/prettydelete/{{ i.id }}/">删除</a>
                </td>
            </tr>
        {% endfor %} 
    
        <div>
                 {{ page_string }}
        </div>
"""


class Pageination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 浏览器请求
        :param queryset: 数据库查询到的对象集合
        :param page_size: 一页要显示多少条数据
        :param page_param: 在url中分页参数的名字，例如/pretty/list/?page=3
        :param plus: 页码前后的显示范围，例如5表示前后显示各5页
        :return:
        """
        # 用来保证原来的搜索条件不变，直接把页码接在后面添加一个page=num
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.page_param = page_param

        self.start = (page - 1) * page_size
        self.end = page * page_size
        # 这里返回相应的应该显示的范围的数据
        self.page_queryset = queryset[self.start: self.end]
        # 计算总页码的数量
        self.sqlcount = queryset.count()
        count, div = divmod(self.sqlcount, self.page_size)
        # 若有余， 总页数还得再加一，比如603条数据有61页
        if div:
            count += 1
        # count: 总页数，比如总共61页
        self.count = count
        self.plus = plus

    def html(self):
        if self.count <= (2 * self.plus + 1):
            # 若总页数小于允许一次显示的范围（比如允许一次显示10页）
            # 那起始页面就是1，结束页面就是总的页码数量
            start_page = 1
            end_page = self.count
        else:
            # 页面有多余时
            if self.page <= self.plus:
                # 因为范围为page - plus， 所以要判断page和plus的大小
                # 当页码小于极小值时，最小值为1，最大值就是允许显示plus * 2 + 1
                start_page = 1
                end_page = (self.plus * 2 + 1)
            else:
                # 当前页+plus大于总页面时，最大值为总页面数，
                if (self.page + self.plus) > self.count:
                    start_page = self.count - 2 * self.plus
                    end_page = self.count
                else:
                    # 否则就是一个正常的范围
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus


        page_str_list = ['<ul class="pagination">']
        # 首页的添加
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页，当前页大于1才使上一页是减一
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 添加页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 同理，尾页和下一页的添加
        if self.page < self.count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nex = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.count])
            nex = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nex)
        self.query_dict.setlist(self.page_param, [self.count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        page_str_list.append('</ul>')
        page_string = mark_safe("".join(page_str_list))

        return page_string
