from django import forms
from django.db.models import get_model
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms import ChoiceField, MultipleChoiceField
from smart_selects.widgets import ChainedSelect, ChainedSelectMultiple


class ChainedField(object):
    """
    Dummy field to distinguish smart select fields in form.
    """
    def _get_queryset_choices(self, value):
        if self.widget.app_name is None:
            return
        model_class = get_model(self.widget.app_name, self.widget.model_name)
        keywords = {self.widget.model_field: value}
        if self.widget.manager is not None and hasattr(model_class, self.widget.manager):
            queryset = getattr(model_class, self.widget.manager)
        else:
            queryset = model_class._default_manager
        return queryset.filter(**keywords)
 
    def clean_form(self, field_name, form_cleaned_data):
        queryset = self._get_queryset_choices(form_cleaned_data[self.widget.chain_field])
        if queryset is None:
            return
        if not queryset.filter(id__in=form_cleaned_data.get('index_var_list', [])).exists():
            raise forms.ValidationError("There is no such choice")


class ChainedChoiceField(ChainedField, ChoiceField):

    def __init__(self, chain_field, show_all=False, auto_choose=True,
                 initial=None, view_name=None, choices=None, *args, **kwargs):
        defaults = {
            'widget': ChainedSelect(chain_field=chain_field, show_all=show_all,
                auto_choose=auto_choose, view_name=view_name, choices=choices),
        }
        defaults.update(kwargs)
        super(ChainedChoiceField, self).__init__(choices=choices, initial=initial, *args, **defaults)


class ChainedMultipleChoiceField(ChainedField, MultipleChoiceField):

    def __init__(self, chain_field, show_all=False, auto_choose=True,
                 initial=None, view_name=None, choices=None, *args, **kwargs):
        defaults = {
            'widget': ChainedSelectMultiple(chain_field=chain_field, show_all=show_all,
                auto_choose=auto_choose, view_name=view_name, choices=choices),
        }
        defaults.update(kwargs)
        super(ChainedMultipleChoiceField, self).__init__(choices=choices, initial=initial, *args, **defaults)


class ChainedModelChoiceField(ChainedField, ModelChoiceField):

    def __init__(self, app_name, model_name,
                 chain_field, model_field, show_all=False,
                 auto_choose=True, manager=None,
                 initial=None, view_name=None, *args, **kwargs):
        defaults = {
            'widget': ChainedSelect(app_name, model_name, chain_field,
                                    model_field, show_all, auto_choose,
                                    manager, view_name),
        }
        defaults.update(kwargs)
        if not 'queryset' in kwargs:
            queryset = get_model(app_name, model_name).objects.all()
            super(ChainedModelChoiceField, self).__init__(queryset=queryset, initial=initial, **defaults)
        else:
            super(ChainedModelChoiceField, self).__init__(initial=initial, *args, **defaults)


class ChainedModelMultipleChoiceField(ChainedField, ModelMultipleChoiceField):

    def __init__(self, app_name, model_name,
                 chain_field, model_field, show_all=False,
                 auto_choose=True, manager=None,
                 initial=None, view_name=None, *args, **kwargs):
        defaults = {
            'widget': ChainedSelectMultiple(app_name, model_name, chain_field,
                                    model_field, show_all, auto_choose,
                                    manager, view_name, verbose_name=kwargs.get('label')),
        }
        defaults.update(kwargs)
        if not 'queryset' in kwargs:
            queryset = get_model(app_name, model_name).objects.all()
            super(ChainedModelMultipleChoiceField, self).__init__(queryset=queryset, initial=initial, **defaults)
        else:
            super(ChainedModelMultipleChoiceField, self).__init__(initial=initial, *args, **defaults)


class GroupedModelSelect(ChainedField, ModelChoiceField):
    def __init__(self, queryset, order_field, *args, **kwargs):
        self.order_field = order_field
        super(GroupedModelSelect, self).__init__(queryset, *args, **kwargs)

    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices
        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh QuerySetIterator that has not been
        # consumed. Note that we're instantiating a new QuerySetIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        group_indexes = {}
        choices = [("", self.empty_label or "---------")]
        i = len(choices)
        for item in self.queryset:
            order_field = getattr(item, self.order_field)
            group_index = order_field.pk
            if not group_index in group_indexes:
                group_indexes[group_index] = i
                choices.append([unicode(order_field), []])
                i += 1
            choice_index = group_indexes[group_index]
            choices[choice_index][1].append(self.make_choice(item))
        return choices

    def make_choice(self, obj):
        return obj.pk, "   " + self.label_from_instance(obj)

    choices = property(_get_choices, ChoiceField._set_choices)
