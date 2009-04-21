from django.conf.urls.defaults import *

urlpatterns = patterns('chained_selects.views',
    url(r'^(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain', name='chained_filter'),
)