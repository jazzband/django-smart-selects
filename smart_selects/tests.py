import unittest
from unittest.mock import MagicMock

from .db_fields import ChainedForeignKey, GroupedForeignKey
from .widgets import ChainedSelect


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


class ChainedSelectWidgetTests(unittest.TestCase):
    def test_render_with_zero_value(self):
        widget = ChainedSelect(
            to_app_name="app",
            to_model_name="model",
            chained_field="parent",
            chained_model_field="parent",
            foreign_key_app_name="app",
            foreign_key_model_name="model",
            foreign_key_field_name="child",
            show_all=False,
            auto_choose=True,
        )
        widget.queryset = MagicMock()
        choice_mock = MagicMock()
        choice_mock.pk = 0
        choice_mock.__str__.return_value = "ZeroChoice"
        widget._get_available_choices = MagicMock(return_value=[choice_mock])
        rendered = widget.render("field", 0)
        self.assertIn('data-value="0"', rendered)
        self.assertIn('value="0"', rendered)
        self.assertIn("ZeroChoice", rendered)
        widget._get_available_choices.assert_called_once()
