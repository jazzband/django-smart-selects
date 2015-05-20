from django.http import HttpResponse

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
    
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from smart_selects.utils import (get_keywords, sort_results, serialize_results,
                                 get_queryset)


def filterchain(request, app, model, field, value, manager=None):
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)
    queryset = get_queryset(model_class, manager)

    results = queryset.filter(**keywords)

    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        results = list(results)
        sort_results(results)

    serialized_results = serialize_results(results)
    results_json = json.dumps(serialized_results)
    return HttpResponse(results_json, content_type='application/json')


def filterchain_all(request, app, model, field, value):
    """Returns filtered results followed by excluded results below."""

    model_class = get_model(app, model)
    keywords = get_keywords(field, value)
    queryset = get_queryset(model_class)

    filtered = list(queryset.filter(**keywords))
    sort_results(filtered)

    excluded = list(queryset.exclude(**keywords))
    sort_results(excluded)

    # Empty choice to separate filtered and excluded results.
    empty_choice = {'value': "", 'display': "---------"}

    serialized_results = (
        serialize_results(filtered) +
        [empty_choice] +
        serialize_results(excluded)
    )

    results_json = json.dumps(serialized_results)
    return HttpResponse(results_json, content_type='application/json')
