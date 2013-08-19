/*jslint indent: 4, maxlen: 120 */
/*global $: false, document, jQuery, django, navigator, windowname_to_id */

/* Used in the ChainedSelect widget. Looks for all chained select inputs, uses their extra elements to build AJAX
   queries for those inputs, based on the given fields' values, and then deletes the data elements. */
(function ($) {
    "use strict";
    $('div.field-smart-select-data').each(function () {
        var dismissAddAnotherPopup,
            oldDismissAddAnotherPopup,
            chained_field = this.getAttribute('data-chained-field'),
            url = this.getAttribute('data-url'),
            value = this.getAttribute('data-value'),
            auto_choose = this.getAttribute('data-auto-choose') === 'True',
            empty_label = this.getAttribute('data-empty-label'),
            $chained_field = $('#id_' + chained_field),
            $select_box = $('#' + this.getAttribute('data-id'));
        console.log('Are you seeing this?!');
        $(document).ready(function () {
            var val;
            function fill_field(val, init_value) {
                var options;
                if (!val || val === '') {
                    options = '<option value="">' + empty_label + '</option>';
                    $select_box.html(options);
                    $select_box.children('option:first').attr('selected', 'selected');
                    $select_box.trigger('change');
                    return;
                }
                $.getJSON(url + '/' + val + '/', function (j) {
                    var width,
                        i;
                    options = '<option value="">' + empty_label + '</option>';
                    for (i = 0; i < j.length; i += 1) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '</option>';
                    }
                    width = $select_box.outerWidth();
                    $select_box.html(options);
                    if (navigator.appVersion.indexOf('MSIE') !== -1) {
                        $select_box.width(width + 'px');
                    }
                    $select_box.children('option:first').attr('selected', 'selected');
                    if (init_value) {
                        $select_box.children('option[value="' + init_value + '"]').attr('selected', 'selected');
                    }
                    if (auto_choose && j.length === 1) {
                        $select_box.children('option[value="' + j[0].value + '"]').attr('selected', 'selected');
                    }
                    $select_box.trigger('change');
                });
            }
            if (!$chained_field.hasClass('chained')) {
                val = $chained_field.val();
                fill_field(val, value);
            }
            $chained_field.change(function () {
                var start_value = $select_box.val();
                val = $(this).val();
                fill_field(val, start_value);
            });
        });
        if (dismissAddAnotherPopup !== undefined) {
            oldDismissAddAnotherPopup = dismissAddAnotherPopup;
            dismissAddAnotherPopup = function (win, newId, newRepr) {
                oldDismissAddAnotherPopup(win, newId, newRepr);
                if (windowname_to_id(win.name) === 'id_' + chained_field) {
                    $chained_field.change();
                }
            };
        }
    });
}(jQuery || django.jQuery));
