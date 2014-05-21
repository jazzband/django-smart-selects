# -*- coding: utf-8 -*-
from locale import strcoll
from django.db.models import get_model


def unicode_sorter(key_input):
    """ This function implements sort keys for the german language according to 
    DIN 5007."""
    
    # key1: compare words lowercase and replace umlauts according to DIN 5007
    key1 = key_input.lower()
    key1 = key1.replace(u"ä", u"a")
    key1 = key1.replace(u"ö", u"o")
    key1 = key1.replace(u"ü", u"u")
    key1 = key1.replace(u"ß", u"ss")
    
    # key2: sort the lowercase word before the uppercase word and sort
    # the word with umlaut after the word without umlaut
    #key2=input.swapcase()
    
    # in case two words are the same according to key1, sort the words
    # according to key2. 
    return key1

def get_filterchain_kwargs(field, value):
    if value == '0':
        return {str("%s__isnull" % field): True}
    return {str(field): str(value)}

def get_filterchain_queryset(app, model, manager=None):
    model_class = get_model(app, model)
    if manager is not None and hasattr(model_class, manager):
        return getattr(model_class, manager)
    return model_class._default_manager

def render_filterchain_choices(item_queryset):
    item_list = list(item_queryset)
    item_list.sort(cmp=strcoll, key=lambda x: unicode_sorter(unicode(x)))
    return [{'value': item.pk, 'display': unicode(item)} for item in item_list]
