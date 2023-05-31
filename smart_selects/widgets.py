import json

from django.apps import apps
from django.conf import settings

from django.urls import reverse
from django.forms.widgets import Select, SelectMultiple, Media
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
from django.utils.html import escape

from smart_selects.utils import unicode_sorter, sort_results

get_model = apps.get_model

USE_DJANGO_JQUERY = getattr(settings, "USE_DJANGO_JQUERY", False)
JQUERY_URL = getattr(
    settings,
    "JQUERY_URL",
    "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js",
)

URL_PREFIX = getattr(settings, "SMART_SELECTS_URL_PREFIX", "")


class JqueryMediaMixin:
    @property
    def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(JqueryMediaMixin, self).media

        js = []

        if JQUERY_URL:
            js.append(JQUERY_URL)
        elif JQUERY_URL is not False:
            vendor = "vendor/jquery/"
            extra = "" if settings.DEBUG else ".min"

            jquery_paths = [
                "{}jquery{}.js".format(vendor, extra),
                "jquery.init.js",
            ]

            if USE_DJANGO_JQUERY:
                jquery_paths = ["admin/js/{}".format(path) for path in jquery_paths]

            js.extend(jquery_paths)

        media += Media(js=js)
        return media


class ChainedSelect(JqueryMediaMixin, Select):
    def __init__(
        self,
        to_app_name,
        to_model_name,
        chained_field,
        chained_model_field,
        foreign_key_app_name,
        foreign_key_model_name,
        foreign_key_field_name,
        show_all,
        auto_choose,
        sort=True,
        manager=None,
        view_name=None,
        *args,
        **kwargs
    ):
        self.to_app_name = to_app_name
        self.to_model_name = to_model_name
        self.chained_field = chained_field
        self.chained_model_field = chained_model_field
        self.show_all = show_all
        self.auto_choose = auto_choose
        self.sort = sort
        self.manager = manager
        self.view_name = view_name
        self.foreign_key_app_name = foreign_key_app_name
        self.foreign_key_model_name = foreign_key_model_name
        self.foreign_key_field_name = foreign_key_field_name
        super(Select, self).__init__(*args, **kwargs)

    @property
    def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(ChainedSelect, self).media
        js = [
            "smart-selects/admin/js/chainedfk.js",
            "smart-selects/admin/js/bindfields.js",
        ]
        media += Media(js=js)
        return media

    # TODO: Simplify this and remove the noqa tag
    def render(self, name, value, attrs=None, choices=(), renderer=None):  # noqa: C901
        if len(name.split("-")) > 1:  # formset
            chained_field = "-".join(name.split("-")[:-1] + [self.chained_field])
        else:
            chained_field = self.chained_field

        if not self.view_name:
            if self.show_all:
                view_name = "chained_filter_all"
            else:
                view_name = "chained_filter"
        else:
            view_name = self.view_name
        kwargs = {
            "app": self.to_app_name,
            "model": self.to_model_name,
            "field": self.chained_model_field,
            "foreign_key_app_name": self.foreign_key_app_name,
            "foreign_key_model_name": self.foreign_key_model_name,
            "foreign_key_field_name": self.foreign_key_field_name,
            "value": "1",
        }
        if self.manager is not None:
            kwargs.update({"manager": self.manager})
        url = URL_PREFIX + ("/".join(reverse(view_name, kwargs=kwargs).split("/")[:-2]))
        if self.auto_choose:
            auto_choose = "true"
        else:
            auto_choose = "false"
        if choices:
            iterator = iter(self.choices)
            if hasattr(iterator, "__next__"):
                empty_label = iterator.__next__()[1]
            else:
                # Hacky way to getting the correct empty_label from the field instead of a hardcoded '--------'
                empty_label = iterator.next()[1]
        else:
            empty_label = "--------"

        final_choices = []

        if value:
            available_choices = self._get_available_choices(self.queryset, value)
            for choice in available_choices:
                final_choices.append((choice.pk, force_str(choice)))
        if len(final_choices) > 1:
            final_choices = [("", (empty_label))] + final_choices
        if self.show_all:
            final_choices.append(("", (empty_label)))
            self.choices = list(self.choices)
            if self.sort:
                self.choices.sort(key=lambda x: unicode_sorter(x[1]))
            for ch in self.choices:
                if ch not in final_choices:
                    final_choices.append(ch)
        elif final_choices == []:
            final_choices.append(("", (empty_label)))
        self.choices = final_choices

        attrs.update(self.attrs)
        attrs["data-chainfield"] = chained_field
        attrs["data-url"] = url
        attrs["data-value"] = "null" if value is None or value == "" else value
        attrs["data-auto_choose"] = auto_choose
        attrs["data-empty_label"] = escape(empty_label)
        final_attrs = self.build_attrs(attrs)
        if "class" in final_attrs:
            final_attrs["class"] += " chained-fk"
        else:
            final_attrs["class"] = "chained-fk"

        if renderer:
            output = super(ChainedSelect, self).render(
                name, value, final_attrs, renderer
            )
        else:
            output = super(ChainedSelect, self).render(name, value, final_attrs)

        return mark_safe(output)

    def _get_available_choices(self, queryset, value):
        """
        get possible choices for selection
        """
        item = queryset.filter(pk=value).first()
        if item:
            try:
                pk = getattr(item, self.chained_model_field + "_id")
                filter = {self.chained_model_field: pk}
            except AttributeError:
                try:  # maybe m2m?
                    pks = (
                        getattr(item, self.chained_model_field)
                        .all()
                        .values_list("pk", flat=True)
                    )
                    filter = {self.chained_model_field + "__in": pks}
                except AttributeError:
                    try:  # maybe a set?
                        pks = (
                            getattr(item, self.chained_model_field + "_set")
                            .all()
                            .values_list("pk", flat=True)
                        )
                        filter = {self.chained_model_field + "__in": pks}
                    except AttributeError:  # give up
                        filter = {}
            filtered = list(
                get_model(self.to_app_name, self.to_model_name)
                .objects.filter(**filter)
                .distinct()
            )
            if self.sort:
                sort_results(filtered)
        else:
            # invalid value for queryset
            filtered = []

        return filtered


class ChainedSelectMultiple(JqueryMediaMixin, SelectMultiple):
    def __init__(
        self,
        to_app_name,
        to_model_name,
        chain_field,
        chained_model_field,
        foreign_key_app_name,
        foreign_key_model_name,
        foreign_key_field_name,
        auto_choose,
        horizontal,
        verbose_name="",
        manager=None,
        *args,
        **kwargs
    ):
        self.to_app_name = to_app_name
        self.to_model_name = to_model_name
        self.chain_field = chain_field
        self.chained_model_field = chained_model_field
        self.auto_choose = auto_choose
        self.horizontal = horizontal
        self.verbose_name = verbose_name
        self.manager = manager
        self.foreign_key_app_name = foreign_key_app_name
        self.foreign_key_model_name = foreign_key_model_name
        self.foreign_key_field_name = foreign_key_field_name
        super(SelectMultiple, self).__init__(*args, **kwargs)

    @property
    def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(ChainedSelectMultiple, self).media
        js = []
        if self.horizontal:
            # For horizontal mode add django filter horizontal javascript code
            js.extend(
                [
                    "admin/js/core.js",
                    "admin/js/SelectBox.js",
                    "admin/js/SelectFilter2.js",
                ]
            )
        js.extend(
            [
                "smart-selects/admin/js/chainedm2m.js",
                "smart-selects/admin/js/bindfields.js",
            ]
        )
        media += Media(js=js)
        return media

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if len(name.split("-")) > 1:  # formset
            chain_field = "-".join(name.split("-")[:-1] + [self.chain_field])
        else:
            chain_field = self.chain_field

        view_name = "chained_filter"

        kwargs = {
            "app": self.to_app_name,
            "model": self.to_model_name,
            "field": self.chained_model_field,
            "foreign_key_app_name": self.foreign_key_app_name,
            "foreign_key_model_name": self.foreign_key_model_name,
            "foreign_key_field_name": self.foreign_key_field_name,
            "value": "1",
        }
        if self.manager is not None:
            kwargs.update({"manager": self.manager})
        url = URL_PREFIX + ("/".join(reverse(view_name, kwargs=kwargs).split("/")[:-2]))
        if self.auto_choose:
            auto_choose = "true"
        else:
            auto_choose = "false"

        # since we cannot deduce the value of the chained_field
        # so we just render empty choices here and let the js
        # fetch related choices later
        final_choices = []
        self.choices = final_choices

        attrs.update(self.attrs)
        attrs["data-chainfield"] = chain_field
        attrs["data-url"] = url
        attrs["data-value"] = "null" if value is None else json.dumps(value)
        attrs["data-auto_choose"] = auto_choose
        attrs["name"] = name
        final_attrs = self.build_attrs(attrs)
        if "class" in final_attrs:
            final_attrs["class"] += " chained"
        else:
            final_attrs["class"] = "chained"
        if self.horizontal:
            # For hozontal mode add django filter horizontal javascript selector class
            final_attrs["class"] += " selectfilter"
        final_attrs["data-field-name"] = self.verbose_name
        if renderer:
            output = super(ChainedSelectMultiple, self).render(
                name, value, final_attrs, renderer
            )
        else:
            output = super(ChainedSelectMultiple, self).render(name, value, final_attrs)

        return mark_safe(output)
