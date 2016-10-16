from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.core import serializers

import json

from .models import BlogsPost
from .models import Person

from .models import Genotype
from .models import Mouse
from .models import Mate

# test form
from .forms import NameForm

# test table
# from table.views import FeedDataView
from .tables import GenotypeTable
from .tables import MouseTable
from .tables import MateTable


class IndexView(TemplateView):
    template_name = 'index.html'


def blog(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('blog.html', {'blog_list': blog_list})


# api
# 发出get的响应
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


# 接收POST请求数据
from .models import Choice, Question


def mouse_table_edit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse(
                'polls:results', args=(question.id, )))


# statistic
def statistic(request):
    statistic_list = BlogsPost.objects.all()
    return render_to_response('statistic.html',
                              {'statistic_list': statistic_list})


# datatable
def GenotypeTableView(request):
    table = GenotypeTable()
    return render(request, "datatable.html", {'search_table': table})


def MouseTableView(request):
    table = MouseTable()
    return render(request, "datatable.html", {'search_table': table})


def MateTableView(request):
    table = MateTable()
    return render(request, "datatable.html", {'search_table': table})


def BootstrapTableView(request):
    return render(request, "bootstraptable.html")

#class BootstrapTableView(TemplateView):
#    template_name = 'bootstraptable.html'


def mouse_profile(request, uid):
    person = get_object_or_404(Person, pk=uid)
    return HttpResponse("User %s" % person.name)

# class MouseDataView(FeedDataView):
#
#    token = MouseTable.token
#
#    def get_queryset(self):
#        return super(MouseDataView, self).get_queryset().filter(id__gt=5)


# plot chart example
class ChartView(TemplateView):
    template_name = 'chart_template.html'


# dynamic api example
class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'


def server_info_api(request):
    server_info = {'cpu': 99,
                   'memory': 30,
                   'network': 44,
                   'disk': 55, }
    return HttpResponse(json.dumps(server_info))
