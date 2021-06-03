from django.urls import re_path
from smart_selects import views

urlpatterns = [
    re_path(
        r"^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$",  # noqa: E501
        views.filterchain_all,
        name="chained_filter_all",
    ),
    re_path(
        r"^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$",  # noqa: E501
        views.filterchain,
        name="chained_filter",
    ),
    re_path(
        r"^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-,]+)/$",  # noqa: E501
        views.filterchain,
        name="chained_filter",
    ),
]
