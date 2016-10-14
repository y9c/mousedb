from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import TemplateView

import json

from .models import BlogsPost
from .models import Person
from .models import Genotype
from .models import Mouse
from .models import Mate

# test form
from .forms import NameForm

# test table
from table.views import FeedDataView
from .tables import GenotypeTable
from .tables import MouseTable
from .tables import MateTable


class IndexView(TemplateView):
    template_name = 'index.html'


def blog(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('blog.html', {'blog_list': blog_list})


# api
def mouse_count_api(request):
    mouse_count = {'mouse': Mouse.objects.count()}
    return HttpResponse(json.dumps(mouse_count))


# statistic
def statistic(request):
    statistic_list = BlogsPost.objects.all()
    return render_to_response('statistic.html', {'statistic_list': statistic_list})


# datatable

def genotype_table(request):
    table = GenotypeTable()
    return render(request, "datatable.html", {'mouse': table})


def mouse_table(request):
    table = MouseTable()
    return render(request, "datatable.html", {'mouse': table})


def mouse_profile(request, uid):
    person = get_object_or_404(Person, pk=uid)
    return HttpResponse("User %s" % person.name)


class MouseDataView(FeedDataView):

    token = MouseTable.token

    def get_queryset(self):
        return super(MouseDataView, self).get_queryset().filter(id__gt=5)


# plot chart example
class ChartView(TemplateView):
    template_name = 'chart_template.html'


# dynamic api example
class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'


def server_info_api(request):
    server_info = {'cpu': 99, 'memory': 30, 'network': 44, 'disk': 55, }
    server_info = get_server_info()
    return HttpResponse(json.dumps(server_info))

