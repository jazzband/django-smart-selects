from json import dumps
from django.http import HttpResponse

from .utils import get_filterchain_kwargs, get_filterchain_queryset, \
    render_filterchain_choices


def filterchain(request, app, model, field, value, manager=None):
    filter_kwargs = get_filterchain_kwargs(field, value)
    filter_queryset = get_filterchain_queryset(app, model, manager)

    rendered_choices = render_filterchain_choices(filter_queryset.filter(**filter_kwargs))
    return HttpResponse(dumps(rendered_choices), mimetype='application/json')

def filterchain_all(request, app, model, field, value, manager=None):
    filter_kwargs = get_filterchain_kwargs(field, value)
    filter_queryset = get_filterchain_queryset(app, model, manager)

    rendered_choices = render_filterchain_choices(filter_queryset.filter(**filter_kwargs))
    rendered_choices.append({'value': "", 'display': "---------"})
    rendered_choices += render_filterchain_choices(filter_queryset.exclude(**filter_kwargs))
    return HttpResponse(dumps(rendered_choices), mimetype='application/json')
