# -*- coding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, \
    ChainedManyToManyField, GroupedForeignKey


class Continent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Area(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Location(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    country = ChainedForeignKey(
        'Country',
        chained_field="continent",
        chained_model_field="continent",
        show_all=False,
        auto_choose=True
    )
    area = ChainedForeignKey(
        'Area',
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True
    )
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)


# test limit_to_choice field option
class Location1(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
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
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    writer = ChainedManyToManyField(
        Writer,
        chained_field="publication",
        chained_model_field="publications",
        horizontal=True,
        )
    name = models.CharField(max_length=255)


# test limit_to_choice field option
class Book1(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
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
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    team = GroupedForeignKey(Team, 'grade')


# The following scenario causes a null initial value in the js in ChainedManyToManyFields

class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Domain(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name


class Website(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    domains = ChainedManyToManyField(
        Domain,
        chained_field='client',
        chained_model_field='client')

    def __str__(self):
        return "%s" % self.name


# test filter when chained_field not is a ForeignKeyField
KIND_CHOICES = (
    ('music', 'Music'),
    ('video', 'Video'),
)


class Tag(models.Model):
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    slug = models.SlugField(max_length=60)

    def __str__(self):
        return "%s" % self.slug


class TagResource(models.Model):
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    tag = ChainedForeignKey(
        Tag,
        chained_field='kind',
        chained_model_field='kind',
        show_all=False,
        auto_choose=True
    )

    def __str__(self):
        return "%s - %s" % (self.kind, self.tag.slug)


# Test many to many with inlines and formsets
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return "%s" % self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return "%s" % self.name


class Talent(models.Model):
    name = models.CharField(max_length=64)
    persons = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        return "%s" % self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    talents = ChainedManyToManyField(
        Talent,
        chained_field='person',
        chained_model_field='persons',
        horizontal=True
    )
    date_joined = models.DateField()
