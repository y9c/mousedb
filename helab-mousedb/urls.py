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
    url(r'^api/server-info-api$',
        views.server_info_api, name='server_info_api'),
    url(r'^api/mouse-count-api$',
        views.mouse_count_api, name='mouse_count_api'),
    url(r'^api/mouse-table-api$',
        views.mouse_table_api, name='mouse_table_api'),
    url(r'^api/mouse-(?P<mouse_pk>[0-9]+)-detail-api$',
        views.mouse_detail_api, name='mouse_detail_api'),


    #  show statistic
    url(r'^chart-exmaple/$', views.ChartView.as_view(), name='chart-demo'),
    url(r'^statistic/', views.StatisticView),

    # show datetable
    url(r'^datatable$', views.BootstrapTableView, name='bootstrap_table'),

    # demos to learn
    url(r'^dynamic-exmaple/$', views.DynamicView.as_view(), name='dynamic'),
    url(r'^media/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

]
