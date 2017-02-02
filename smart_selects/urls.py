from smart_selects import views
try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

urlpatterns = [
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain_all, name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$',  # noqa: E501
        views.filterchain, name='chained_filter'),
]
