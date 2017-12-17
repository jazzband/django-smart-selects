import django
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    (url(r'^admin/', include(admin.site.urls)) if django.VERSION < (2, 0)
     else url(r'^admin/', admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
]
