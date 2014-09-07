import locale

from django.db.models import get_model
from django.http import HttpResponse
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from smart_selects.utils import unicode_sorter


def filterchain(request, app, model, field, value, manager=None):
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)

    if manager is not None and hasattr(model_class, manager):
        queryset = getattr(model_class, manager)
    else:
        queryset = model_class._default_manager

    results = queryset.filter(**keywords)

    if not getattr(model_class._meta, 'ordering', False):
        results = list(results)
        sort_results(results)

    serialized_results = serialize_results(results)
    results_json = json.dumps(serialized_results)
    return HttpResponse(results_json, content_type='application/json')


def filterchain_all(request, app, model, field, value):
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)

    filtered = list(model_class._default_manager.filter(**keywords))
    sort_results(filtered)
    final = serialize_results(filtered)

    excluded = list(model_class._default_manager.exclude(**keywords))
    sort_results(excluded)
    final.append({'value': "", 'display': "---------"})

    final.extend(serialize_results(excluded))
    final_json = json.dumps(final)
    return HttpResponse(final_json, content_type='application/json')


def serialize_results(results):
    return [
        {'value': item.pk, 'display': unicode(item)} for item in results
    ]


def get_keywords(field, value):
    if value == '0':
        keywords = {str("%s__isnull" % field): True}
    else:
        keywords = {str(field): str(value)}

    return keywords


def sort_results(results):
    """Performs in-place sort of filterchain results."""

    results.sort(cmp=locale.strcoll, key=lambda x: unicode_sorter(unicode(x)))
