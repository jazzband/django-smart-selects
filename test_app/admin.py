# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Continent, Country, Location, Publication, Book, Writer


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('continent', 'country', 'city', 'street')


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WriterAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Writer, WriterAdmin)
