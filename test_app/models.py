# -*- coding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField, GroupedForeignKey


class Continent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Location(models.Model):
    continent = models.ForeignKey(Continent)
    country = ChainedForeignKey(
        'Country',
        chained_field="continent",
        chained_model_field="continent",
        show_all=False,
        auto_choose=True
    )
    # area = ChainedForeignKey(Area, chained_field="country", chained_model_field="country")
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)


# test limit_to_choice field option
class Location1(models.Model):
    continent = models.ForeignKey(Continent)
    country = ChainedForeignKey(
        'test_app.Country',
        chained_field="continent",
        chained_model_field="continent",
        show_all=False,
        auto_choose=True,
        limit_choices_to={'name__startswith': 'G'}
    )
    # area = ChainedForeignKey(Area, chained_field="country", chained_model_field="country")
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)


class Publication(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Writer(models.Model):
    name = models.CharField(max_length=255)
    publications = models.ManyToManyField('Publication', blank=True)

    def __str__(self):
        return "%s" % self.name


class Book(models.Model):
    publication = models.ForeignKey(Publication)
    writer = ChainedManyToManyField(
        Writer,
        chained_field="publication",
        chained_model_field="publications",
        )
    name = models.CharField(max_length=255)


# test limit_to_choice field option
class Book1(models.Model):
    publication = models.ForeignKey(Publication)
    writer = ChainedManyToManyField(
        'Writer',
        chained_field="publication",
        chained_model_field="publications",
        limit_choices_to={'name__contains': '2'}
        )
    name = models.CharField(max_length=255)


# group foreignkey
class Grade(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ForeignKey(Grade)

    def __str__(self):
        return "%s" % self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ForeignKey(Grade)
    team = GroupedForeignKey(Team, 'grade')


# The following scenario causes a null initial value in the js in ChainedManyToManyFields

class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Domain(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client)

    def __str__(self):
        return "%s" % self.name


class Website(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client)
    domains = ChainedManyToManyField(Domain, chained_field='client', chained_model_field='client')

    def __str__(self):
        return "%s" % self.name
