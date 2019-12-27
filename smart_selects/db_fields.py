import django
from django.db.models.fields.related import (
    ForeignKey, ManyToManyField, RECURSIVE_RELATIONSHIP_CONSTANT
)
from django.db import models

import six

from smart_selects import form_fields


class IntrospectiveFieldMixin(object):
    to_app_name = None
    to_model_name = None

    def __init__(self, to, *args, **kwargs):
        if isinstance(to, six.string_types):
            if to == RECURSIVE_RELATIONSHIP_CONSTANT:  # to == 'self'
                # This will be handled in contribute_to_class(), when we have
                # enough information to set these properly
                self.to_app_name, self.to_model_name = (None, to)
            elif '.' in to:  # 'app_label.ModelName'
                self.to_app_name, self.to_model_name = to.split('.')
            else:  # 'ModelName'
                self.to_app_name, self.to_model_name = (None, to)
        else:
            self.to_app_name = to._meta.app_label
            self.to_model_name = to._meta.object_name

        super(IntrospectiveFieldMixin, self).__init__(to, *args, **kwargs)

    def contribute_to_class(self, cls, *args, **kwargs):
        if self.to_model_name == RECURSIVE_RELATIONSHIP_CONSTANT:
            # Resolve the model name
            self.to_model_name = cls._meta.object_name
        if self.to_app_name is None:
            # Resolve the app name
            self.to_app_name = cls._meta.app_label
        super(IntrospectiveFieldMixin, self).contribute_to_class(cls, *args, **kwargs)


class ChainedManyToManyField(IntrospectiveFieldMixin, ManyToManyField):
    """
    chains the choices of a previous combo box with this ManyToMany
    """
    def __init__(self, to, chained_field=None, chained_model_field=None,
                 auto_choose=False, horizontal=False, **kwargs):
        """
        examples:

        class Publication(models.Model):
            name = models.CharField(max_length=255)

        class Writer(models.Model):
            name = models.CharField(max_length=255)
            publications = models.ManyToManyField('Publication', blank=True, null=True)

        class Book(models.Model):
            publication = models.ForeignKey(Publication)
            writer = ChainedManyToManyField(
                Writer,
                chained_field="publication",
                chained_model_field="publications",
                )
            name = models.CharField(max_length=255)

        ``chained_field`` is the name of the ForeignKey field referenced by ChainedManyToManyField of the same Model.
        in the examples, chained_field is the name of field publication in Model Book.

        ``chained_model_field`` is the name of the ManyToMany field referenced in the 'to' Model.
        in the examples, chained_model_field is the name of field publications in Model Writer.

        ``auto_choose`` controls whether auto select the choice when there is only one available choice.

        """
        self.chain_field = chained_field
        self.chained_model_field = chained_model_field
        self.auto_choose = auto_choose
        self.horizontal = horizontal
        self.verbose_name = kwargs.get('verbose_name', '')
        super(ChainedManyToManyField, self).__init__(to, **kwargs)

    def deconstruct(self):
        field_name, path, args, kwargs = super(
            ChainedManyToManyField, self).deconstruct()

        # Maps attribute names to their default kwarg values.
        defaults = {
            'chain_field': None,
            'chained_model_field': None,
            'auto_choose': False,
            'horizontal': False
        }

        # Maps attribute names to their __init__ kwarg names.
        attr_to_kwarg_names = {
            'chain_field': 'chained_field',
            'chained_model_field': 'chained_model_field',
            'auto_choose': 'auto_choose',
            'horizontal': 'horizontal',
            'verbose_name': 'verbose_name'
        }

        for name, default in defaults.items():
            value = getattr(self, name)
            kwarg_name = attr_to_kwarg_names[name]

            # None and Boolean defaults should use an 'is' comparison.
            if value is not default:
                kwargs[kwarg_name] = value
            else:
                # value is default, so don't include it in serialized kwargs.
                if kwarg_name in kwargs:
                    del kwargs[kwarg_name]

        return field_name, path, args, kwargs

    def formfield(self, **kwargs):
        foreign_key_app_name = self.model._meta.app_label
        foreign_key_model_name = self.model._meta.object_name
        foreign_key_field_name = self.name
        defaults = {
            'form_class': form_fields.ChainedManyToManyField,
            'queryset': (self.rel.to._default_manager.complex_filter(
                self.rel.limit_choices_to) if django.VERSION < (2, 0) else
                self.remote_field.model._default_manager.complex_filter(
                    self.remote_field.limit_choices_to)),
            'to_app_name': self.to_app_name,
            'to_model_name': self.to_model_name,
            'chain_field': self.chain_field,
            'chained_model_field': self.chained_model_field,
            'auto_choose': self.auto_choose,
            'horizontal': self.horizontal,
            'verbose_name': self.verbose_name,
            'foreign_key_app_name': foreign_key_app_name,
            'foreign_key_model_name': foreign_key_model_name,
            'foreign_key_field_name': foreign_key_field_name,
        }
        defaults.update(kwargs)
        return super(ChainedManyToManyField, self).formfield(**defaults)


class ChainedForeignKey(IntrospectiveFieldMixin, ForeignKey):
    """
    chains the choices of a previous combo box with this one
    """
    def __init__(self, to, chained_field=None, chained_model_field=None,
                 show_all=False, auto_choose=False, sort=True, view_name=None, **kwargs):
        """
        examples:

        class Continent(models.Model):
            name = models.CharField(max_length=255)

        class Country(models.Model):
            continent = models.ForeignKey(Continent)

        class Location(models.Model):
            continent = models.ForeignKey(Continent)
            country = ChainedForeignKey(
                Country,
                chained_field="continent",
                chained_model_field="continent",
                show_all=True,
                auto_choose=True,
                sort=True,
                # limit_choices_to={'name':'test'}
            )
        ``chained_field`` is the name of the ForeignKey field referenced by ChainedForeignKey of the same Model.
        in the examples, chained_field is the name of field continent in Model Location.

        ``chained_model_field`` is the name of the ForeignKey field referenced in the 'to' Model.
        in the examples, chained_model_field is the name of field continent in Model Country.

        ``show_all`` controls whether show other choices below the filtered choices, with separater '----------'.

        ``auto_choose`` controls whether auto select the choice when there is only one available choice.

        ``sort`` controls whether or not to sort results lexicographically or not.

        ``view_name`` controls which view to use, 'chained_filter' or 'chained_filter_all'.

        """
        self.chained_field = chained_field
        self.chained_model_field = chained_model_field
        self.show_all = show_all
        self.auto_choose = auto_choose
        self.sort = sort
        self.view_name = view_name
        if kwargs:
            kwargs['on_delete'] = kwargs.get('on_delete', models.CASCADE)
        else:
            kwargs = {'on_delete': models.CASCADE}
        super(ChainedForeignKey, self).__init__(to, **kwargs)

    def deconstruct(self):
        field_name, path, args, kwargs = super(
            ChainedForeignKey, self).deconstruct()

        # Maps attribute names to their default kwarg values.
        defaults = {
            'chained_field': None,
            'chained_model_field': None,
            'show_all': False,
            'auto_choose': False,
            'sort': True,
            'view_name': None,
        }

        # Maps attribute names to their __init__ kwarg names.
        attr_to_kwarg_names = {
            'chained_field': 'chained_field',
            'chained_model_field': 'chained_model_field',
            'show_all': 'show_all',
            'auto_choose': 'auto_choose',
            'sort': 'sort',
            'view_name': 'view_name',
        }

        for name, default in defaults.items():
            value = getattr(self, name)
            kwarg_name = attr_to_kwarg_names[name]

            # None and Boolean defaults should use an 'is' comparison.
            if value is not default:
                kwargs[kwarg_name] = value
            else:
                # value is default, so don't include it in serialized kwargs.
                if kwarg_name in kwargs:
                    del kwargs[kwarg_name]

        return field_name, path, args, kwargs

    def formfield(self, **kwargs):
        foreign_key_app_name = self.model._meta.app_label
        foreign_key_model_name = self.model._meta.object_name
        foreign_key_field_name = self.name
        defaults = {
            'form_class': form_fields.ChainedModelChoiceField,
            'queryset': (self.rel.to._default_manager.complex_filter(
                self.rel.limit_choices_to) if django.VERSION < (2, 0) else
                self.remote_field.model._default_manager.complex_filter(
                    self.remote_field.limit_choices_to)),
            'to_field_name': (self.rel.field_name if django.VERSION < (2, 0)
                              else self.remote_field.field_name),
            'to_app_name': self.to_app_name,
            'to_model_name': self.to_model_name,
            'chained_field': self.chained_field,
            'chained_model_field': self.chained_model_field,
            'show_all': self.show_all,
            'auto_choose': self.auto_choose,
            'sort': self.sort,
            'view_name': self.view_name,
            'foreign_key_app_name': foreign_key_app_name,
            'foreign_key_model_name': foreign_key_model_name,
            'foreign_key_field_name': foreign_key_field_name,
        }
        defaults.update(kwargs)
        return super(ChainedForeignKey, self).formfield(**defaults)


class GroupedForeignKey(ForeignKey):
    """
    Opt Grouped Field
    """
    def __init__(self, to, group_field, **kwargs):
        self.group_field = group_field
        self._choices = True
        if kwargs:
            kwargs['on_delete'] = kwargs.get('on_delete', models.CASCADE)
        else:
            kwargs = {'on_delete': models.CASCADE}
        super(GroupedForeignKey, self).__init__(to, **kwargs)

    def deconstruct(self):
        field_name, path, args, kwargs = super(
            GroupedForeignKey, self).deconstruct()

        # Add positional arg group_field as a kwarg, since the 'to' positional
        # arg is serialized as a keyword arg by the superclass deconstruct().
        kwargs.update(group_field=self.group_field)

        # Choices handling in Field.deconstruct() should suffice (if choices is
        # not default, serialize it as a kwarg). _choices is set in the
        # GroupedForeignKey constructor, but should be overwritten by the
        # Field constructor's handling of the 'choices' kwarg.

        return field_name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.GroupedModelSelect,
            'queryset': (self.rel.to._default_manager.complex_filter(
                self.rel.limit_choices_to) if django.VERSION < (2, 0) else
                self.remote_field.model._default_manager.complex_filter(
                    self.remote_field.limit_choices_to)),
            'to_field_name': (self.rel.field_name if django.VERSION < (2, 0)
                              else self.remote_field.field_name),
            'order_field': self.group_field,
        }
        defaults.update(kwargs)
        return super(ForeignKey, self).formfield(**defaults)
