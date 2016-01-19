# -*- coding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField


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
        Country,
        chained_field="continent",
        chained_model_field="continent",
        show_all=False,
        auto_choose=True
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
