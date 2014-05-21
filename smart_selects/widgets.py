import locale
from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe
from smart_selects.utils import unicode_sorter


if getattr(settings, 'USE_DJANGO_JQUERY', True):
    USE_DJANGO_JQUERY = True
else:
    USE_DJANGO_JQUERY = False
    JQUERY_URL = getattr(settings, 'JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')

URL_PREFIX = getattr(settings, 'SMART_SELECTS_URL_PREFIX', '')


class ChainedSelect(Select):
    def __init__(self, app_name=None, model_name=None, chain_field=None,
                 model_field=None, show_all=None, auto_choose=None,
                 manager=None, view_name=None, choices=None, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.chain_field = chain_field
        self.model_field = model_field
        self.show_all = show_all
        self.auto_choose = auto_choose
        self.manager = manager
        self.view_name = view_name
        self.choices = choices
        super(ChainedSelect, self).__init__(*args, **kwargs)

    class Media:
        if USE_DJANGO_JQUERY:
            js = [static('admin/%s' % i) for i in
                  ('js/jquery.min.js', 'js/jquery.init.js')]
        elif JQUERY_URL:
            js = [JQUERY_URL]
        else:
            js = []
        js.append('/static/js/smart_selects.js')

    def get_queryset(self, value):
        return get_model(self.app_name, self.model_name).objects

    def render(self, name, value, attrs=None, choices=()):
        if len(name.split('-')) > 1:  # formset
            chain_field = '-'.join(name.split('-')[:-1] + [self.chain_field])
        else:
            chain_field = self.chain_field

        if not self.view_name:
            kwargs = {'app': self.app_name, 'model': self.model_name,
                      'field': self.model_field, 'value': '1'}
            if self.show_all:
                view_name = 'chained_filter_all'
            else:
                view_name = 'chained_filter'
        else:
            kwargs = {'value': '1'}
            view_name = self.view_name

        if self.manager is not None:
            kwargs.update({'manager': self.manager})

        url = URL_PREFIX + ('/'.join(reverse(view_name, kwargs=kwargs).split('/')[:-2]))
        if self.allow_multiple_selected:
            empty_label = None
        else:
            # Hacky way to getting the correct empty_label from the field instead of a hardcoded '--------'
            empty_label = iter(self.choices).next()[1]
        if isinstance(value, (list, tuple, set)):
            html_init_values = ','.join(value)
        else:
            html_init_values = unicode(value)
        data_div = '<div class="field-smart-select-data" style="display: none" data-chained-field="%s" data-url="%s" ' \
                   'data-init-values="%s" data-auto-choose="%s" data-empty-label="%s" data-id="%s"></div>' \
                   % (chain_field, url, html_init_values, self.auto_choose, empty_label or '', attrs['id'])
        if self.app_name:
            # if Model field
            if empty_label:
                final_choices = [('', empty_label)]
            else:
                final_choices = []
        else:
            # if non-Model field
            final_choices = self.choices
        if self.show_all:
            final_choices.append(('', empty_label))
            for ch in self.choices:
                if not ch in final_choices:
                    final_choices.append(ch)
        self.choices = []
        final_attrs = self.build_attrs(attrs, name=name)
        if 'class' in final_attrs:
            final_attrs['class'] += ' chained'
        else:
            final_attrs['class'] = 'chained'
        output = super(ChainedSelect, self).render(name, value, final_attrs, choices=final_choices)
        output += data_div
        return mark_safe(output)


from django.contrib.admin.widgets import FilteredSelectMultiple
class ChainedSelectMultiple(ChainedSelect, FilteredSelectMultiple):
    
    def __init__(self, *args, **kwargs):
        defaults = {
            'is_stacked': False,
        }
        defaults.update(kwargs)
        super(ChainedSelectMultiple, self).__init__(*args, **defaults)

