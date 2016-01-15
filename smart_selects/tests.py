import unittest

import django

from .db_fields import ChainedForeignKey, GroupedForeignKey


def has_new_migrations():
    return (django.VERSION[:2] >= (1, 7),
            "This test requires Django migrations introduced in Django 1.7.")


class AssertReconstructibleMixin(object):
    def assert_reconstructible(self, *field_args, **field_kwargs):
        field_instance = self.field_class(*field_args, **field_kwargs)
        name, path, args, kwargs = field_instance.deconstruct()
        new_instance = self.field_class(*args, **kwargs)

        for attr_name in self.deconstruct_attrs:
            self.assertEqual(
                getattr(field_instance, attr_name),
                getattr(new_instance, attr_name)
            )


@unittest.skipUnless(*has_new_migrations())
class ChainedForeignKeyTests(AssertReconstructibleMixin, unittest.TestCase):
    def setUp(self):
        self.field_class = ChainedForeignKey
        self.deconstruct_attrs = [
            'chained_field', 'chained_model_field', 'show_all', 'auto_choose',
            'view_name',
        ]

    def test_deconstruct_basic(self):
        self.assert_reconstructible(
            'myapp.MyModel',
            chained_field='a_chained_field',
            chained_model_field='the_chained_model_field',
            show_all=False, auto_choose=True
        )

    def test_deconstruct_mostly_default(self):
        self.assert_reconstructible(
            'myapp.MyModel'
        )

    def test_deconstruct_non_default(self):
        self.assert_reconstructible(
            'myapp.MyModel',
            chained_field='a_chained_field',
            chained_model_field='the_chained_model_field',
            show_all=True, auto_choose=True
        )


@unittest.skipUnless(*has_new_migrations())
class GroupedForeignKeyTests(AssertReconstructibleMixin, unittest.TestCase):
    def setUp(self):
        self.field_class = GroupedForeignKey
        self.deconstruct_attrs = ['group_field']

    def test_deconstruct_basic(self):
        self.assert_reconstructible('myapp.MyModel', 'the_group_field')
