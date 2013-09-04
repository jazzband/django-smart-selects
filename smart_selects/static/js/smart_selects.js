/*jslint indent: 4, maxlen: 120 */
/*global $: false, window, document, jQuery, django, navigator */

// TODO: get rid of this hack when Django 1.6
if ($.fn.jquery === '1.4.2') {
    $.noConflict(true);
}

/* Used in the ChainedSelect widget. Looks for all chained select inputs, uses their extra elements to build AJAX
   queries for those inputs, based on the given fields' values, and then deletes the data elements. */
(function ($) {
    "use strict";
    function add_chaining_handlers() {
        $('div.field-smart-select-data').each(function () {
            var chained_field = this.getAttribute('data-chained-field'),
                url = this.getAttribute('data-url'),
                auto_choose = this.getAttribute('data-auto-choose') === 'True',
                empty_label = this.getAttribute('data-empty-label'),
                $el = $(this),
                $select_box = $el.siblings('select').eq(0),
            // handle the case where the field is from an inline template being added
                $chained_field = $('#id_' + chained_field.replace('__prefix__', $select_box.attr('id').split('-')[1])),
                is_tabular = this.parentNode.tagName.toLowerCase() === 'td',
                $field_set = $el.closest(is_tabular ? 'tr' : 'fieldset'),
                $object_block = is_tabular ? $field_set : $field_set.parent(),
                is_template = !$object_block.is(':visible') && $object_block.hasClass('empty-form');
            // If we have a template, don't do anything - we need to reuse the data
            if (is_template) {
                return;
            }
            $el.remove();
            $chained_field.change(function () {
                var init_value = $select_box.val(),
                    val = $(this).val(),
                    options;
                if (!val || val === '') {
                    options = '<option value="">' + empty_label + '</option>';
                    $select_box.html(options);
                    $select_box.children('option:first').attr('selected', 'selected');
                    // Add default selected data if it is not already there
                    if ($select_box.data('defaultSelected') === undefined) {
                        $select_box.data('defaultSelected', '');
                    }
                    $select_box.trigger('change');
                    return;
                }
                $.getJSON(url + '/' + val + '/', function (j) {
                    var i;
                    options = '<option value="">' + empty_label + '</option>';
                    for (i = 0; i < j.length; i += 1) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '</option>';
                    }
                    $select_box.html(options);
                    $select_box.children('option:first').attr('selected', 'selected');
                    if (init_value) {
                        $select_box.children('option[value="' + init_value + '"]').attr('selected', 'selected');
                    }
                    if (auto_choose && j.length === 1) {
                        $select_box.children('option[value="' + j[0].value + '"]').attr('selected', 'selected');
                    }
                    // Add default selected data if it is not already there
                    if ($select_box.data('defaultSelected') === undefined) {
                        $select_box.data('defaultSelected', $select_box.val());
                    }
                    $select_box.trigger('change');
                });
            });
            $chained_field.change();
        });
    }
    $(function () {
        // Add all current chained selects
        add_chaining_handlers();
        // Check for new inline chained selects
        window.setTimeout(
            function () {
                $('#content-main').children('form').get(0).addEventListener("DOMNodeInserted", function (e) {
                    var element = e.target;
                    if (element.tagName.toLowerCase() === 'tr' ||
                        (' ' + element.className + ' ').indexOf(' inline-related ') > -1) {
                        add_chaining_handlers();
                    }
                }, false);
            },
            500
        );
    });
}(jQuery || django.jQuery));
