# Django Smart Selects

[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)
[![Build Status](https://github.com/jazzband/django-smart-selects/workflows/Test/badge.svg)](https://github.com/jazzband/django-smart-selects/actions)
[![Coverage Status](https://codecov.io/gh/jazzband/django-smart-selects/branch/master/graph/badge.svg)](https://codecov.io/gh/jazzband/django-smart-selects)
[![PyPI](https://img.shields.io/pypi/v/django-smart-selects.svg)](https://pypi.org/project/django-smart-selects/)

This package allows you to quickly filter or group "chained" models by adding a custom foreign key or many to many field to your models. This will use an AJAX query to load only the applicable chained objects.

Works with Django version 3.2 to 5.0.

**Warning**: The AJAX endpoint enforces no permissions by default.  This means that **any model with a chained field will be world readable**. If you would like more control over this permission, the [`django-autocomplete-light`](https://github.com/yourlabs/django-autocomplete-light) package is a great, high-quality package that enables the same functionality with permission checks.

## Documentation

For more information on installation and configuration see the documentation at:

https://django-smart-selects.readthedocs.io/

## Reporting issues / sending PRs

You can try the test_app example using:

```shell
python manage.py migrate
python manage.py loaddata test_app/fixtures/*
python manage.py runserver
```

Then login with admin/admin at http://127.0.0.1:8000/admin/


## TODO

* Add permission checks to enable users to restrict who can use the chained fields.
* Add a `ChainedCheckboxSelectMultiple` widget and adjust `chainedm2m.js` and `chainedfk.js` to build checkboxes in that case
