import json

from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.core import serializers


from .models import BlogsPost
from .models import Genotype
from .models import Mouse
from .models import Mate

# test form
from .forms import NameForm


class IndexView(TemplateView):
    template_name = 'index.html'


# blog page
def blog(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('blog.html', {'blog_list': blog_list})


# api
# 发出get的响应
# demo
def server_info_api(request):
    server_info = {'cpu': 99,
                   'memory': 30,
                   'network': 44,
                   'disk': 55, }
    return HttpResponse(json.dumps(server_info))


def mouse_count_api(request):
    mouse_count = {'mouse': Mouse.objects.count()}
    return HttpResponse(json.dumps(mouse_count))


def mouse_table_api(request):
    data = serializers.serialize("json", Mouse.objects.all())
    #struct = json.loads(data)
    #data = json.dumps(struct)
    return HttpResponse(data)


def mouse_detail_api(request, mouse_pk):
    mouse = Mouse.objects.get(pk = mouse_pk)
    genotype = mouse.genotype.all()[0:1]
    genotype = serializers.serialize("json", genotype)
    return HttpResponse(genotype)


def mate_table_api(request):
    data = serializers.serialize("json", Mate.objects.all())
    return HttpResponse(data)


# 接收POST请求数据
def mouse_table_edit(request):
    #print(request)
    pass


# statistic
# use echarts
# dynamic chart example
class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'


# chart demo
class ChartView(TemplateView):
    template_name = 'chart_template.html'


def StatisticView(request):
    statistic_list = BlogsPost.objects.all()
    return render_to_response('statistic.html',
                              {'statistic_list': statistic_list})


# datatable
# use bootstraptable
def BootstrapTableView(request):
    return render(request, "datatable.html")
