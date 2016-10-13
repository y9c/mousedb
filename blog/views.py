
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.utils.lorem_ipsum import words
from django.template import RequestContext

from django.contrib.admin.views.decorators import staff_member_required


from django_tables2 import RequestConfig

from random import choice
import json

from .models import BlogsPost
# test table
from .models import Mouse
from .forms import NameForm


class IndexView(TemplateView):
    template_name = 'index.html'


def blog(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('blog.html', {'blog_list': blog_list})


# plot chart example
class ChartView(TemplateView):
    template_name = 'chart_template.html'


# dynamic api example


class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'


def server_info_api(request):
    server_info = get_server_info()
    return HttpResponse(json.dumps(server_info))


def get_server_info():
    server_info = {'cpu': 99, 'memory': 30, 'network': 44, 'disk': 55, }
    return server_info


# table example
def bootstrap_table(request):
    '''Demonstrate the use of the bootstrap table template'''

    table = BootstrapTable(Mouse.objects.all(), order_by='-mouse_id')
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    return render(request, 'table_template.html', {
        'table': table
    })


from table.views import FeedDataView

from .tables import BootstrapTable
from .tables import (
    ModelTable, AjaxTable, AjaxSourceTable,
    CalendarColumnTable, SequenceColumnTable,
    LinkColumnTable, CheckboxColumnTable
)


def base(request):
    table = ModelTable()
    return render(request, "datatable.html", {'people': table})


def ajax(request):
    table = AjaxTable()
    return render(request, "datatable.html", {'people': table})


def ajax_source(request):
    table = AjaxSourceTable()
    return render(request, "datatable.html", {'people': table})


class Foo(object):

    def __init__(self, id, name, calendar):
        self.id = id
        self.name = name
        self.calendar = calendar


def sequence_column(request):
    data = [
        Foo(1, 'A', [1, 2, 3, 4, 5]),
        Foo(2, 'B', [1, 2, 3, 4, 5]),
        Foo(3, 'C', [1, 2, 3, 4, 5])
    ]
    table = SequenceColumnTable(data)
    return render(request, "datatable.html", {'people': table})


def calendar_column(request):
    data = [
        Foo(1, 'A', range(1, 14)),
        Foo(2, 'B', range(1, 14)),
        Foo(3, 'C', range(1, 14))
    ]
    table = CalendarColumnTable(data)
    return render(request, "datatable.html", {'people': table})


def link_column(request):
    table = LinkColumnTable()
    return render(request, "datatable.html", {'people': table})


def checkbox_column(request):
    table = CheckboxColumnTable()
    return render(request, "datatable.html", {'people': table})


def user_profile(request, uid):
    from app.models import Person
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    person = get_object_or_404(Person, pk=uid)
    return HttpResponse("User %s" % person.name)


class MyDataView(FeedDataView):

    token = AjaxSourceTable.token

    def get_queryset(self):
        return super(MyDataView, self).get_queryset().filter(id__gt=5)
