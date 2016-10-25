import json
import datetime

from django.core import serializers
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import BlogsPost
from .models import Breed
from .models import Genotype
from .models import Mouse


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


def getlist_genotype(request):
    field = request.GET.get("field")
    # param = request.GET.get("param")
    strain = request.GET.get("strain")
    line = request.GET.get("line")
    locus = request.GET.get("locus")
    data = Genotype.objects.all()
    if strain is not None:
        data = data.filter(strain=strain)
    if line is not None:
        data = data.filter(line=line)
    if line is not None:
        data = data.filter(locus=locus)
    response_data = {i: i for i in data.values_list(field, flat=True)}
    return HttpResponse(json.dumps(response_data))


def getlist_breed(request):
    try:
        breed = Breed.objects.all()
        data_list = breed.values_list('name', flat=True)
        data_dict = {i: i for i in data_list}
        return HttpResponse(json.dumps(data_dict))
    except:
        data = {'S(XY)': 'S(XY)',
                'S(XX)': 'S(XX)',
                'S(??)': 'S(??)', }
        return HttpResponse(json.dumps(data))


# datatable
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
        mouse = Mouse.objects.all()
        data = serializers.serialize("json", mouse)
        return HttpResponse(data)


# fields
def getlist_mouse_field(request):
    field = request.GET.get("field")
    param = request.GET.get("param")
    if field is not None:
        if param == "choices":
            try:
                choices = dict(Mouse._meta.get_field(field).choices)
                return HttpResponse(json.dumps(choices))
            except:
                return HttpResponse("no such field")
        else:
            return HttpResponse("what do you want to do with this field")
    else:
        return HttpResponse("field should be assign")


# details
def mouse_detail_api(request, mouse_pk):
    mouse = Mouse.objects.get(pk=mouse_pk)
    details = {"Line": mouse.genotype.line, "Locus": mouse.genotype.locus, "Age": mouse.age()}
    details = json.dumps([details])
    return HttpResponse(details)


# statistic: count idle mouse
def mouse_count_api(request):
    status = request.GET.get("status")
    mouse_count = {'mouse': Mouse.objects.filter(status=status).count()}
    return HttpResponse(json.dumps(mouse_count))


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
        print(request.POST)

        details = {"status": "success", "mouse_add": 0}

        # !!!!! add mouse
        # induction
        induct_list = json.loads(request.POST.get("inductRows", "{}"))
        print(induct_list)
        if type(induct_list) == list:
            for row in induct_list:
                m = Mouse()
                # genotype = row["Gen"]
                genotype = "C57BL/6:CRE:C(II)S(XY)"
                strain, line, locus = genotype.split(":")
                genotype_set = Genotype.objects.filter(strain=strain)
                mouse_set = Mouse.objects.filter(genotype__in=genotype_set)
                mouse_id_set = mouse_set.values_list('mouse_id', flat=True)
                mouse_id = "L{}-{0:03d}".format(
                    genotype_set[0].line_id(), max([int(i.split("-")[1]) for i in mouse_id_set])+1
                )
                print(mouse_id)
                print(row["inductSource"])
                print(datetime.datetime.strptime(row["inductDate"] , "%Y-%m-%d") - datetime.timedelta(days=row["Age"]*7))
                details["mouse_add"] += 1

        # genotyping
        genotyping_list = json.loads(request.POST.get("genotypingRows", "{}"))
        print(genotyping_list)
        if type(genotyping_list) == list:
            for row in genotyping_list:
                print("bbbbbbbbbbbbbbb")
                print(row)
                details["mouse_add"] += 1

        # !!!!! edit mouse
        # weighting
        # phenotyping
        # feed
        # drug
        # !!!!! add and edit breed
        # mate
        mate_list = json.loads(request.POST.get("mateRows", "{}"))
        if type(mate_list) == list:
            for row in mate_list:
                print("ccccccccccccccccccc")
                print(row)
                try:
                    mouse_pa = Mouse.objects.get(mouse_id=row["MOUSE-Pa"])
                    mouse_ma = Mouse.objects.get(mouse_id=row["MOUSE-Ma"])
                    if mouse_pa.genotype.sex() == "Male" and mouse_ma.genotype.sex() == "Female":
                        mate_start_date = datetime.datetime.strptime(row["DATE"] , "%Y-%m-%d")
                        if Breed.objects.filter(parent=mouse_pa).filter(parent=mouse_ma).filter(
                                mate_start_date=mate_start_date).count() == 0:
                            # create breed and write to models
                            print("hello")
                            print(mate_start_date)
                        else:
                            print("ERROR: breed already exist")
                    else:
                        print("ERROR: wrong sex combination, you many input the wrong mouse id")

                except:
                    print("ERROR: the mouse not exsit")

        # separate
        separate_list = json.loads(request.POST.get("separateRows", "{}"))
        if type(separate_list) == list:
            for row in separate_list:
                print("dddddddddddddddddddddd")
                print(row)
                try:
                    breed = Breed.objects.get(name=row["MATE"])
                    mate_end_date = datetime.datetime.strptime(row["DATE"] , "%Y-%m-%d")
                    print("hello")
                    print(breed)
                    print(mate_end_date)
                except:
                    print("ERROR: mate name dose not exist!!")

        # born
        # ablactation

        #    print(breed.mate_start_date)
        #    details["mate_start_date"] = str(breed.mate_start_date)
        #    details["mate_end_date"] = str(breed.mate_end_date)
        #    details["born_date"] = str(breed.born_date)
        #    details = json.dumps(details)
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


def statistic_view(request):
    statistic_list = BlogsPost.objects.all()
    return render_to_response('statistic.html',
                              {'statistic_list': statistic_list})


# datatable
# use bootstraptable
def datatable_view(request):
    return render(request, "datatable.html")


# event
# use form
def event_view(request):
    return render(request, 'events.html')


def event_add_view(request):
    return render(request, 'events/add.html')


def event_edit_view(request):
    return render(request, 'events/edit.html')


def event_breed_view(request):
    return render(request, 'events/breed.html')


# render
# use echarts
class RenderView(TemplateView):
    template_name = 'render.html'
