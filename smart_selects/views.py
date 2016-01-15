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
                                 get_queryset, get_limit_choices_to)


def is_m2m(model_class, field):
    try:
        from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor
        is_pre_19_syntax = True
    except ImportError:
        from django.db.models.fields.related import ManyToManyDescriptor
        is_pre_19_syntax = False

    if is_pre_19_syntax:
        if isinstance(getattr(model_class, field), ReverseManyRelatedObjectsDescriptor):
            return True
    else:
        if isinstance(getattr(model_class, field), ManyToManyDescriptor) and \
           not getattr(model_class, field).reverse:
            return True

    return False


def filterchain(request, app, model, field, foreign_key_app_name, foreign_key_model_name,
                foreign_key_field_name, value, manager=None):
    model_class = get_model(app, model)
    m2m = is_m2m(model_class, field)
    keywords = get_keywords(field, value, m2m=m2m)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, manager, limit_choices_to)

    results = queryset.filter(**keywords)

    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        results = list(results)
        sort_results(results)

    serialized_results = serialize_results(results)
    results_json = json.dumps(serialized_results)
    return HttpResponse(results_json, content_type='application/json')


def filterchain_all(request, app, model, field, foreign_key_app_name,
                    foreign_key_model_name, foreign_key_field_name, value):
    """Returns filtered results followed by excluded results below."""
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, limit_choices_to=limit_choices_to)

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
