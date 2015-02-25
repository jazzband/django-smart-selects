# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
import locale
import six
import unicodedata


def unicode_sorter(data):
    """ This function implements sort keys for the german language according to
    DIN 5007."""

    return unicodedata.normalize('NFKD', data.lower()).encode(
        'ascii', 'ignore').decode('ascii')


def get_queryset(model_class, manager=None):
    if manager is not None and hasattr(model_class, manager):
        queryset = getattr(model_class, manager)
    else:
        queryset = model_class._default_manager
    return queryset


def serialize_results(results):
    return [
        {'value': item.pk, 'display': force_text(item)} for item in results
    ]


def get_keywords(field, value):
    if value == '0':
        keywords = {str("%s__isnull" % field): True}
    else:
        keywords = {str(field): str(value)}

    return keywords


def sort_results(results):
    """Performs in-place sort of filterchain results."""
    results.sort(key=lambda x: unicode_sorter(force_text(x)))


