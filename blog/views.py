
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
from .models import Country, Person
from .tables import BootstrapTable


class IndexView(TemplateView):
    template_name = 'index.html'


def blog(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('blog.html', {'blog_list': blog_list})


# test table


def create_fake_data():
    # create some fake data to make sure we need to paginate
    if Person.objects.all().count() < 50:
        countries = list(Country.objects.all()) + [None]
        Person.objects.bulk_create([
            Person(name=words(3, common=False), country=choice(countries))
            for i in range(50)
        ])


def bootstrap(request):
    '''Demonstrate the use of the bootstrap template'''

    create_fake_data()
    table = BootstrapTable(Person.objects.all(), order_by='-name')
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    return render(request, 'bootstrap_template.html', {
        'table': table
    })



class DynamicView(TemplateView):
    template_name = 'dynamic_template.html'

def server(request):
    context = {
        'title': u'服务器负载情况',
    }
    return render_to_response('dynamic_template.html', context, context_instance=RequestContext(request))


def server_info_api(request):
    server_info = get_server_info()
    return HttpResponse(json.dumps(server_info))


def get_server_info():
    server_info = {'cpu': 99, 'memory': 30, 'network': 44, 'disk': 55,}
    return server_info
