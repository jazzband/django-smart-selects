from django.db.models import get_model
from django.forms.models import ModelChoiceField
from django.forms import ChoiceField

from smart_selects.widgets import ChainedSelect


class ChainedModelChoiceField(ModelChoiceField):

    def __init__(self, app_name, model_name,
                 chain_field, model_field, show_all,
                 auto_choose, manager=None,
                 initial=None, view_name=None, *args, **kwargs):
        defaults = {
            'widget': ChainedSelect(app_name, model_name, chain_field,
                                    model_field, show_all, auto_choose,
                                    manager, view_name),
        }
        defaults.update(kwargs)
        if not 'queryset' in kwargs:
            queryset = get_model(app_name, model_name).objects.all()
            super(ChainedModelChoiceField, self).__init__(queryset=queryset, initial=initial, *args, **defaults)
        else:
            super(ChainedModelChoiceField, self).__init__(initial=initial, *args, **defaults)

    def _get_choices(self):
        self.widget.queryset = self.queryset
        choices = super(ChainedModelChoiceField, self)._get_choices()
        return choices
    choices = property(_get_choices, ChoiceField._set_choices)


class GroupedModelSelect(ModelChoiceField):
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
        return (obj.pk, "   " + self.label_from_instance(obj))

    choices = property(_get_choices, ChoiceField._set_choices)
