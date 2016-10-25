# coding: utf-8

from table.columns.linkcolumn import Column , LinkColumn , ImageLink
from table import Table
from table.utils import A

from .models import Genotype
from .models import Mouse
from .models import Breed

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
    name = Column(field='name', header=u'NAME')
    status = Column(field='status', header=u'STATUS')
    notes = Column(field='notes', header=u'NOTE')
    dob = Column(field='dob', header=u'BIRTH')
    dod = Column(field='dod', header=u'DEAD')

    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='mouse_profile', args=(A('id'),), image=image_url, image_title='avatar')])

    class Meta:
        model = Mouse
        # ajax = True
        # ajax_source = reverse_lazy('ajax_source_api')


class MateTable(Table):
    id = Column(field='mate_id', header=u'ID')
    paid = Column(field='paternal_id', header=u'PA_ID')
    maid = Column(field='maternal_id', header=u'MA_ID')
    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='mouse_profile', args=(A('id'),), image=image_url, image_title='avatar')])

    # logo = ImageColumn(field='logo.url', header=u'Logo Image',
    # image_title='logo')

    class Meta:
        model = Breed
        # ajax = True
        # ajax_source = reverse_lazy('ajax_source_api')
