# coding: utf-8

from datetime import date

from django.urls import reverse_lazy


from table.columns import Column
from table.columns.calendarcolumn import CalendarColumn
from table.columns.sequencecolumn import SequenceColumn
from table.columns.imagecolumn import ImageColumn
from table.columns.linkcolumn import LinkColumn, Link, ImageLink
from table.columns.checkboxcolumn import CheckboxColumn
from table import Table
from table.utils import A

from .models import Person
from .models import Genotype
from .models import Mouse
from .models import Mate


# mouse example

image_url = 'img/user-512.png'

class GenotypeTable(Table):
    strain = Column(field='strain', header=u'STRAIN')
    line = Column(field='line', header=u'LINE')
    locus = Column(field='locus', header=u'LOCUS')
    sex = Column(field='sex', header=u'SEX')

    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='mouse_profile', args=(A('id'),), image=image_url, image_title='avatar')])

    class Meta:
        model = Genotype
        # ajax = True
        # ajax_source = reverse_lazy('ajax_source_api')


class MouseTable(Table):
    id = Column(field='mouse_id', header=u'ID')
    name = Column(field='name', header=u'ID')
    sex = Column(field='sex', header=u'SEX')
    genotype = Column(field='genotype', header=u'GEN')
    sacked = CheckboxColumn(field='sacked', header=u'SAC')

    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='mouse_profile', args=(A('id'),), image=image_url, image_title='avatar')])

    class Meta:
        model = Mouse
        # ajax = True
        # ajax_source = reverse_lazy('ajax_source_api')


class MateTable(Table):
    id = Column(field='mouse_id', header=u'ID')
    sex = Column(field='sex', header=u'SEX')
    organization = Column(field='genotype', header=u'GEN')
    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='mouse_profile', args=(A('id'),), image=image_url, image_title='avatar')])
    # logo = ImageColumn(field='logo.url', header=u'Logo Image',
    # image_title='logo')
    sacked = CheckboxColumn(field='sacked', header=u'SAC')

    class Meta:
        model = Mouse
        # ajax = True
        # ajax_source = reverse_lazy('ajax_source_api')
