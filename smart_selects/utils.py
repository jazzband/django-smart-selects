from django.apps import apps
from django.utils.encoding import force_str

get_model = apps.get_model


def unicode_sorter(input):
    """This function implements sort keys for the german language according to
    DIN 5007."""

    # key1: compare words lowercase and replace umlauts according to DIN 5007
    key1 = input.lower()
    key1 = key1.replace(u"ä", u"a")
    key1 = key1.replace(u"ö", u"o")
    key1 = key1.replace(u"ü", u"u")
    key1 = key1.replace(u"ß", u"ss")

    # key2: sort the lowercase word before the uppercase word and sort
    # the word with umlaut after the word without umlaut
    # key2=input.swapcase()

    # in case two words are the same according to key1, sort the words
    # according to key2.
    return key1


def get_limit_choices_to(app_name, model_name, field_name):
    try:
        model = get_model(app_name, model_name)
        field = model._meta.get_field(field_name)
        limit_choices_to = field.remote_field.limit_choices_to
    except Exception:
        limit_choices_to = None

    return limit_choices_to


def get_queryset(model_class, manager=None, limit_choices_to=None):
    if manager is not None and hasattr(model_class, manager):
        queryset = getattr(model_class, manager)
    else:
        queryset = model_class._default_manager

    if limit_choices_to:
        queryset = queryset.complex_filter(limit_choices_to)
    return queryset


def serialize_results(results):
    return [
        {
            "value": item.pk if str(item.pk).isdigit() else str(item.pk),
            "display": force_str(item),
        }
        for item in results
    ]


def get_keywords(field, value, m2m=False):
    if value == "0":
        keywords = {str("%s__isnull" % field): True}
    elif m2m:
        keywords = {str("%s__pk" % field): str(value)}
    else:
        keywords = {str(field): str(value)}

    return keywords


def sort_results(results):
    """Performs in-place sort of filterchain results."""

    results.sort(key=lambda x: unicode_sorter(force_str(x)))
