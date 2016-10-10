# coding: utf-8
import django_tables2 as tables

from .models import Country, Person


class BootstrapTable(tables.Table):

    country = tables.RelatedLinkColumn()

    class Meta:
        model = Person
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}
        exclude = ('friendly', )
