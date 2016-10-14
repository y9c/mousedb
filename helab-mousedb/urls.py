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

    # api for posting data
    url(r'^api/mouse_count_api$', views.mouse_count_api, name='mouse_count_api'),

    # statistic mouse
    url(r'^chart-exmaple/$', views.ChartView.as_view(), name='chart-demo'),
    url(r'^statistic/', views.statistic),

    # show table
    url(r'^datatable/genotype$', views.genotype_table, name='genotype_table'),
    url(r'^datatable/mouse$', views.mouse_table, name='mouse_table'),
    url(r'^datatable/mate$', views.mouse_table, name='mate_table'),
    url(r'^datatable/api/$',
        views.MouseDataView.as_view(), name='ajax_source_api'),
    url(r'^user/(\d+)/$', views.mouse_profile, name='mouse_profile'),
    url(r'^table/', include('table.urls')),

    # demos to learn
    url(r'^dynamic-exmaple/$', views.DynamicView.as_view(), name='dynamic'),
    url(r'^api/server-info-api$',
        views.server_info_api, name='server_info_api'),
    url(r'^media/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

]
