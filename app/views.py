import json

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.http import Http404

from .models import BlogsPost
from .models import Genotype
from .models import Mouse
from .models import Breed

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
    if request.GET.get("hello") == "1":
        return HttpResponse(json.dumps({"hello": 1}))
    else:
        server_info = {'cpu': 99,
                       'memory': 30,
                       'network': 44,
                       'disk': 55, }
        return HttpResponse(json.dumps(server_info))


def getlist_genotype_locus(request):
    try:
        locus = Genotype.objects.filter(line=request.GET.get("line"))
        #print(locus.locus.all())
        data = serializers.serialize("json", locus)
        return HttpResponse(data)
    except:
        data = {'S(XY)': 'S(XY)',
                'S(XX)': 'S(XX)',
                'S(??)': 'S(??)', }
        return HttpResponse(json.dumps(data))

# statistic: count idle mouse
def mouse_count_api(request):
    status = request.GET.get("status")
    mouse_count = {'mouse': Mouse.objects.filter(status=status).count()}
    return HttpResponse(json.dumps(mouse_count))


def mouse_table_api(request):
    print(request)
    if request.GET.get("rule_query") != '':
        rule_params = request.GET.get("rule_query").split('&')
        try:
            rules = {p.split("=")[0]: p.split("=")[1] for p in rule_params}
            print(rules)
            try:
                mouse = Mouse.objects.filter(**rules)
                data = serializers.serialize("json", mouse)
                return HttpResponse(data)
            except:
                print("null date")
                return HttpResponse("null=date")
        except:
            print("得这么搞 XXX=YYY")
            return HttpResponse("error format")
    else:
        #struct = json.loads(data)
        #data = json.dumps(struct)
        mouse = Mouse.objects.all()
        data = serializers.serialize("json", mouse)
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
        # show post request
        print(request.POST)

        # render response
        selected_mouse = get_object_or_404(Mouse, pk=request.POST.get('pk'))
        setattr(selected_mouse, request.POST.get('field').split(".")[1],
                request.POST.get('edit'))
        selected_mouse.save()
        return HttpResponse("Edit Done!")
    else:
        raise Http404


@csrf_exempt
def mouse_event_submit(request):
    if request.method == 'POST' and request.is_ajax():
        # show post request
        print(request.POST)
        details = {}
        details["breedCount"] =10000000
        if 'breedID' in request.POST:
            details["breedID"] = request.POST.get('breedID')
        if 'breedIDCount' in request.POST:
            details["breedCount"] = request.POST.get('breedCount')
        #    print(breed.mate_start_date)
        #    details["mate_start_date"] = str(breed.mate_start_date)
        #    details["mate_end_date"] = str(breed.mate_end_date)
        #    details["born_date"] = str(breed.born_date)
        #    details = json.dumps(details)
        print("\n",details)
        return HttpResponse(json.dumps(details))
    else:
        raise Http404


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
def EventView(request):
    return render(request, 'events.html')


def EventAddView(request):
    return render(request, 'events/add.html')


def EventEditView(request):
    return render(request, 'events/edit.html')


def EventBreedView(request):
    return render(request, 'events/breed.html')


# render
# use echarts
class RenderView(TemplateView):
    template_name = 'render.html'
