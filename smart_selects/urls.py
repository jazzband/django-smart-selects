try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

urlpatterns = patterns(
    'smart_selects.views',
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        'filterchain_all', name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        'filterchain', name='chained_filter'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        'filterchain', name='chained_filter'),
)
