from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.views import static

from app import views


# admin.autodiscover()
urlpatterns = [
    # admin page for manage
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # index page
    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^blog/', views.blog, name='blog'),

    # api for get date
    url(r'^api/server-info-api$',
        views.server_info_api, name='server_info_api'),
    url(r'^api/getlist-genotype$',
        views.getlist_genotype, name='getlist_genotype'),
    url(r'^api/getlist-breed$',
        views.getlist_breed, name='getlist_breed'),
    url(r'^api/getlist-mouse-field$',
        views.getlist_mouse_field, name='getlist_mouse_field'),
    url(r'^api/mouse-count-api$',
        views.mouse_count_api, name='mouse_count_api'),
    url(r'^api/mouse-table-api$',
        views.mouse_table_api, name='mouse_table_api'),
    url(r'^api/mouse-(?P<mouse_pk>[0-9]+)-detail-api$',
        views.mouse_detail_api, name='mouse_detail_api'),
    # api for posting data
    url(r'^api/mouse-table-edit$',
        views.mouse_table_edit, name='mouse_table_edit'),
    url(r'^api/mouse-event-submit$',
        views.mouse_event_submit, name='mouse_event_submit'),

    # show event
    url(r'^event/$', views.event_view, name='event_page'),
    url(r'^event/add$', views.event_add_view, name='event_add_page'),
    url(r'^event/edit$', views.event_edit_view, name='event_edit_page'),
    url(r'^event/breed$', views.event_breed_view, name='event_breed_page'),

    # show datetable
    url(r'^datatable/$', views.datatable_view, name='datatable_page'),

    #  show statistic
    url(r'^statistic/$', views.statistic_view, name='statistic_page'),

    # show render
    url(r'^render/$', views.RenderView.as_view(), name='render_page'),


    url(r'^chart-exmaple/$', views.ChartView.as_view(), name='chart-demo'),
    url(r'^dynamic-exmaple/$', views.DynamicView.as_view(), name='dynamic'),
    url(r'^media/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

]
