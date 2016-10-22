from django.http import JsonResponse
from django.db.models import Q
from django.utils.six import iteritems
from django.views.decorators.cache import never_cache

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

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


def do_filter(qs, keywords, exclude=False):
    """
    Filter queryset based on keywords.
    Support for multiple-selected parent values.
    """
    and_q = Q()
    for keyword, value in iteritems(keywords):
        values = value.split(",")
        if len(values) > 0:
            or_q = Q()
            for value in values:
                or_q |= Q(**{keyword: value})
            and_q &= or_q
    if exclude:
        qs = qs.exclude(and_q)
    else:
        qs = qs.filter(and_q)
    return qs


@never_cache
def filterchain(request, app, model, field, foreign_key_app_name, foreign_key_model_name,
                foreign_key_field_name, value, manager=None):
    model_class = get_model(app, model)
    m2m = is_m2m(model_class, field)
    keywords = get_keywords(field, value, m2m=m2m)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, manager, limit_choices_to)

    results = do_filter(queryset, keywords)

    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        results = list(results)
        sort_results(results)

    serialized_results = serialize_results(results)
    return JsonResponse(serialized_results, safe=False)


@never_cache
def filterchain_all(request, app, model, field, foreign_key_app_name,
                    foreign_key_model_name, foreign_key_field_name, value):
    """Returns filtered results followed by excluded results below."""
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, limit_choices_to=limit_choices_to)

    filtered = list(do_filter(queryset, keywords))
    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        sort_results(list(filtered))

    excluded = list(do_filter(queryset, keywords, exclude=True))
    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        sort_results(list(excluded))

    # Empty choice to separate filtered and excluded results.
    empty_choice = {'value': "", 'display': "---------"}

    serialized_results = (
        serialize_results(filtered) +
        [empty_choice] +
        serialize_results(excluded)
    )

    return JsonResponse(serialized_results, safe=False)
