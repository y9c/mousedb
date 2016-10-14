"""DjangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.views import static

from blog import views


# admin.autodiscover()
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^media/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^blog/', views.blog),
    # url(r'^blog/', include('blog.urls')),
    url(r'^chart-exmaple/$', views.ChartView.as_view(), name='chart-demo'),
    url(r'^dynamic-exmaple/$', views.DynamicView.as_view(), name='dynamic'),
    url(r'^api/server-info-api$', views.server_info_api, name='server_info_api'),


    url(r'^datatable/$', views.mouse_table, name='mouse_table'),
    url(r'^datatable/api/$', views.MyDataView.as_view(), name='ajax_source_api'),
    url(r'^user/(\d+)/$', views.mouse_profile, name='mouse_profile'),
    url(r'^table/', include('table.urls')),
]
