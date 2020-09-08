import django
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    (path('admin/', include(admin.site.urls)) if django.VERSION < (2, 0)
     else path('admin/', admin.site.urls)),
    path('chaining/', include('smart_selects.urls')),
]
