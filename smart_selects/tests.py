import unittest

from .db_fields import ChainedForeignKey, GroupedForeignKey


class AssertReconstructibleMixin:
    def assert_reconstructible(self, *field_args, **field_kwargs):
        field_instance = self.field_class(*field_args, **field_kwargs)
        name, path, args, kwargs = field_instance.deconstruct()
        new_instance = self.field_class(*args, **kwargs)

        for attr_name in self.deconstruct_attrs:
            self.assertEqual(
                getattr(field_instance, attr_name), getattr(new_instance, attr_name)
            )


class ChainedForeignKeyTests(AssertReconstructibleMixin, unittest.TestCase):
    def setUp(self):
        self.field_class = ChainedForeignKey
        self.deconstruct_attrs = [
            "chained_field",
            "chained_model_field",
            "show_all",
            "auto_choose",
            "view_name",
        ]

    def test_deconstruct_basic(self):
        self.assert_reconstructible(
            "myapp.MyModel",
            chained_field="a_chained_field",
            chained_model_field="the_chained_model_field",
            show_all=False,
            auto_choose=True,
        )

    def test_deconstruct_mostly_default(self):
        self.assert_reconstructible("myapp.MyModel")

    def test_deconstruct_non_default(self):
        self.assert_reconstructible(
            "myapp.MyModel",
            chained_field="a_chained_field",
            chained_model_field="the_chained_model_field",
            show_all=True,
            auto_choose=True,
        )


class GroupedForeignKeyTests(AssertReconstructibleMixin, unittest.TestCase):
    def setUp(self):
        self.field_class = GroupedForeignKey
        self.deconstruct_attrs = ["group_field"]

    def test_deconstruct_basic(self):
        self.assert_reconstructible("myapp.MyModel", "the_group_field")
