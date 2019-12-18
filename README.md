# Django Smart Selects

[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)

[![Build Status](https://travis-ci.org/jazzband/django-smart-selects.svg?branch=master)](https://travis-ci.org/jazzband/django-smart-selects)

[![Coverage Status](https://coveralls.io/repos/github/jazzband/django-smart-selects/badge.svg?branch=master)](https://coveralls.io/github/jazzband/django-smart-selects?branch=master)


This package allows you to quickly filter or group "chained" models by adding a custom foreign key or many to many field to your models. This will use an AJAX query to load only the applicable chained objects.

**Warning**: The AJAX endpoint enforces no permissions by default.  This means that **any model with a chained field will be world readable**. If you would like more control over this permission, the [`django-autocomplete-light`](https://github.com/yourlabs/django-autocomplete-light) package is a great, high-quality package that enables the same functionality with permission checks.

## Documentation

For more information on installation and configuration see the documentation at:

https://django-smart-selects.readthedocs.io/


## TODO

* Add permission checks to enable users to restrict who can use the chained fields.
* Add a `ChainedCheckboxSelectMultiple` widget and adjust `chainedm2m.js` and `chainedfk.js` to build checkboxes in that case
