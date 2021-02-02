import django
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    (
        path("admin/", include(admin.site.urls))
        if django.VERSION < (2, 0)
        else path("admin/", admin.site.urls)
    ),
    path("chaining/", include("smart_selects.urls")),
]
