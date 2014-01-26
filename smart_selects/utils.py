# -*- coding: utf-8 -*-
import unicodedata


def unicode_sorter(input):
    """ This function implements sort keys for the german language according to 
    DIN 5007."""
    return unicodedata.normalize('NFKD', input.lower()).encode('ascii', 'ignore').decode('ascii')
