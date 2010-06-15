from django.conf.urls.defaults import *

urlpatterns = patterns('smart_selects.views',
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain_all', name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain', name='chained_filter'),
)
