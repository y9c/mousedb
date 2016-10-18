import json

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers

from .models import BlogsPost
from .models import Genotype
from .models import Mouse

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
    mouse_count = {'mouse': Mouse.objects.filter(status=0).count()}
    return HttpResponse(json.dumps(mouse_count))


def mouse_table_api(request):
    data = serializers.serialize("json", Mouse.objects.all())
    #struct = json.loads(data)
    #data = json.dumps(struct)
    return HttpResponse(data)


def mouse_detail_api(request, mouse_pk):
    mouse = Mouse.objects.get(pk=mouse_pk)
    details = {}
    details["Line"] = mouse.genotype.line
    details["Locus"] = mouse.genotype.locus
    details["Age"] = mouse.age()
    details = json.dumps([details])
    return HttpResponse(details)


# 接收POST请求数据
@csrf_exempt
def mouse_table_edit(request):
    if request.POST:
        print(request.POST)
        selected_mouse = get_object_or_404(Mouse, pk=request.POST.get('pk'))
        setattr(selected_mouse, request.POST.get('field').split(".")[1],
                request.POST.get('edit'))
        selected_mouse.save()
    else:
        print("error 啊")

    return render(request, 'index.html')


@csrf_exempt
def mouse_event_submit(request):
    if request.POST:
        print(request.POST)
        mouse = Mouse.objects.get(pk=1)
        details = {}
        details["Line"] = mouse.genotype.line
        details["Locus"] = mouse.genotype.locus
        details["Age"] = mouse.age()
        details = json.dumps(details)
        return HttpResponse(details)
    else:
        print("no a post啊")


# statistic
# use echarts
# dynamic chart example
class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'


class ChartView(TemplateView):
    template_name = 'chart_template.html'


def StatisticView(request):
    statistic_list = BlogsPost.objects.all()
    return render_to_response('statistic.html',
                              {'statistic_list': statistic_list})


# datatable
# use bootstraptable
def DatatableView(request):
    return render(request, "datatable.html")


# event
# use form
@csrf_exempt
def EventView(request):
    if request.method == 'POST' and request.is_ajax():
        mouse = Mouse.objects.get(pk=1)
        details = {}

        breedID = request.POST.get('breedID')

        details["Line"] = mouse.genotype.line
        details["Locus"] = mouse.genotype.locus
        details["Age"] = mouse.age()
        details = json.dumps(details)
        return HttpResponse(details)
    return render(request, 'events.html')


# render
# use echarts
class RenderView(TemplateView):
    template_name = 'render.html'
