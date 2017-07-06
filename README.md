# Django Smart Selects

[![Build Status](https://travis-ci.org/digi604/django-smart-selects.svg?branch=master)](https://travis-ci.org/digi604/django-smart-selects)

[![Coverage Status](https://coveralls.io/repos/github/digi604/django-smart-selects/badge.svg?branch=master)](https://coveralls.io/github/digi604/django-smart-selects?branch=master)


This package allows you to quickly filter or group "chained" models by adding a custom foreign key or many to many field to your models. This will use an AJAX query to load only the applicable chained objects.

**Warning**: The AJAX endpoint enforces no permissions by default.  This means that **any model with a chained field will be world readable**. If you would like more control over this permission, the [`django-autocomplete-light`](https://github.com/yourlabs/django-autocomplete-light) package is a great, high-quality package that enables the same functionality with permission checks.

## Chained Selects

Given the following model:

```python
class Continent(models.Model):
    name = models.CharField(max_length=255)

class Country(models.Model):
    continent = models.ForeignKey(Continent)
    name = models.CharField(max_length=255)

class Location(models.Model):
    continent = models.ForeignKey(Continent)
    country = models.ForeignKey(Country)
    area = models.ForeignKey(Area)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
```

Once you select a continent, if you want only the countries on that continent to be available, you can use a `ChainedForeignKey` on the `Location` model:

```python
from smart_selects.db_fields import ChainedForeignKey

class Location(models.Model)
    continent = models.ForeignKey(Continent)
    country = ChainedForeignKey(
        Country,
        chained_field="continent",
        chained_model_field="continent",
        show_all=False,
        auto_choose=True,
        sort=True)
    area = ForeignKey(Area)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
```

### ChainedForeignKey options

#### chained_field (required)

The `chained_field` indicates the field on the same model that should be chained to. In the `Continent`, `Country`, `Location` example, `chained_field` is the name of the field `continent` in model `Location`.

```python
class Location(models.Model)
    continent = models.ForeignKey(Continent)
```

#### chained_model_field (required)

The `chained_model_field` indicates the field of the chained model that corresponds to the model linked to by the `chained_field`. In the `Continent`, `Country`, `Location` example, `chained_model_field` is the name of field `continent` in Model `Country`.

```python
class Country(models.Model):
    continent = models.ForeignKey(Continent)
```

#### show_all (optional)

`show_all` indicates if only the filtered results should be shown or if you also want to display the other results further down.

#### auto_choose (optional)

`auto_choose` indicates if auto select the choice when there is only one available choice.

#### `sort` (optional)

`sort` indicates if the result set should be sorted lexicographically or not. Disable if you want to use the `Model.ordering` option. Defaults to `True`.


## Chained ManyToMany Selects

The `ChainedManyToManyField` works as you would expect:

```python
from smart_selects.db_fields import ChainedManyToManyField

class Publication(models.Model):
    name = models.CharField(max_length=255)

class Writer(models.Model):
    name = models.CharField(max_length=255)
    publications = models.ManyToManyField('Publication', blank=True, null=True)

class Book(models.Model):
    publication = models.ForeignKey(Publication)
    writer = ChainedManyToManyField(
        Writer,
        chained_field="publication",
        chained_model_field="publications")
    name = models.CharField(max_length=255)
```


### Using chained fields in the admin

Do **not** specify the field in the `ModelAdmin` `filter_horizontal` list. Instead, simply pass `horizontal=True` to the `ChainedManyToManyField`:

```python
from smart_selects.db_fields import ChainedManyToManyField

class Publication(models.Model):
    name = models.CharField(max_length=255)

class Writer(models.Model):
    name = models.CharField(max_length=255)
    publications = models.ManyToManyField('Publication', blank=True, null=True)

class Book(models.Model):
    publication = models.ForeignKey(Publication)
    writer = ChainedManyToManyField(
        Writer,
        horizontal=True,
        verbose_name='writer',
        chained_field="publication",
        chained_model_field="publications")
    name = models.CharField(max_length=255)
```


### ChainedManyToManyField options

#### `chained_field` (required)

The `chained_field` indicates the field on the same model that should be chained to. In the `Publication`, `Writer`, `Book` example, `chained_field` is the name of the field `publication` in model `Book`.

```python
class Book(models.Model):
    publication = models.ForeignKey(Publication)
```

#### `chained_model_field` (required)

The `chained_model_field` indicates the field of the chained model that corresponds to the model linked to by the `chained_field`. In the `Publication`, `Writer`, `Book` example, `chained_model_field` is the name of field `publications` in `Writer` model.

```python
class Writer(models.Model):
    publications = models.ManyToManyField('Publication', blank=True, null=True)
```

#### `auto_choose` (optional)

`auto_choose` indicates if auto select the choice when there is only one available choice.

#### `horizontal` (optional)

This option will mixin Django's `FilteredSelectMultiple` to work in the Django admin as you expect


## Grouped Selects

If you have the following model:

```python
class Country(models.Model):
    continent = models.ForeignKey(Continent)

class Location(models.Model):
    continent = models.ForeignKey(Continent)
    country = models.ForeignKey(Country)
```

And you want to group countries by their continent in the HTML select list, you can use a `GroupedForeignKey`:

```python
from smart_selects.db_fields import GroupedForeignKey

class Location(models.Model):
    continent = models.ForeignKey(Continent)
    country = GroupedForeignKey(Country, "continent")
```


## Installation

1. Add `smart_selects` to your `INSTALLED_APPS`
2. Add the `smart_selects` urls into your project's `urls.py`. This is needed for the `Chained Selects` and `Chained ManyToMany Selects`. For example:

    ```python
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^chaining/', include('smart_selects.urls')),
    )
    ```

3. You will also need to include jQuery in every page that includes a field from `smart_selects`, or set `JQUERY_URL = True` in your project's `settings.py`.


## Settings

`JQUERY_URL`
:   jQuery 2.2.0 is loaded from Google's CDN if this is set to `True`. If you would prefer to
    use a different version put the full URL here. Set `JQUERY_URL = False`
    to disable loading jQuery altogether.

`USE_DJANGO_JQUERY`
:   By default, `smart_selects` loads jQuery from Google's CDN. However, it can use jQuery from Django's
    admin area. Set `USE_DJANGO_JQUERY = True` to enable this behaviour.


## TODO

* Add permission checks to enable users to restrict who can use the chained fields.
* Add a `ChainedCheckboxSelectMultiple` widget and adjust `chainedm2m.js` and `chainedfk.js` to build checkboxes in that case
