# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Area, Continent, Country, Location, Publication, \
    Book, Writer, Grade, Team, Student, Client, Domain, Website, \
    Tag, TagResource, Person, Group, Membership, Talent


class WriterAdminInline(admin.TabularInline):
    model = Writer


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('continent', 'country', 'city', 'street')


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WriterAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('slug',)


class TagResourceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GroupAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class TalentAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagResource, TagResourceAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Talent, TalentAdmin)
