(function ($) {
    "use strict";

    window.chainedfk = function () {
        return {
            fireEvent: function (element, event) {
                var evt, rtn;
                if (document.createEventObject) {
                    // dispatch for IE
                    evt = document.createEventObject();
                    rtn = element.fireEvent('on' + event, evt);
                } else {
                    // dispatch for firefox + others
                    evt = document.createEvent("HTMLEvents");
                    evt.initEvent(event, true, true); // event type,bubbling,cancelable
                    rtn = !element.dispatchEvent(evt);
                }

                return rtn;
            },
            dismissRelatedLookupPopup: function (win, chosenId) {
                var name = windowname_to_id(win.name),
                    elem = document.getElementById(name);
                if (elem.className.indexOf('vManyToManyRawIdAdminField') !== -1 && elem.value) {
                    elem.value += ',' + chosenId;
                } else {
                    elem.value = chosenId;
                }
                fireEvent(elem, 'change');
                win.close();
            },
            fill_field: function (val, init_value, elem_id, url, empty_label, auto_choose) {
                var $selectField = $(elem_id),
                    options = [];
                url = url + "/" + val + "/";

                var empty_option =  $('<option></option>')
                    .attr('value', '')
                    .text(empty_label);

                if (!val || val === '') {
                    empty_option.prop('selected', true);
                    options.push(empty_option);

                    $selectField.html(options);
                    $selectField.trigger('change');
                    return;
                }
                $.getJSON(url, function (j) {
                    auto_choose = j.length === 1 && auto_choose;
                    // Append empty label as the first option
                    if (!(init_value || auto_choose)) {
                        empty_option.prop('selected', true);
                    }
                    options.push(empty_option);

                    // Append each option to the select
                    $.each(j, function (index, optionData) {
                        var option = $('<option></option>')
                            .prop('value', optionData.value)
                            .text(optionData.display);
                        if (auto_choose === "true" || auto_choose === "True") {
                            auto_choose = true;
                        } else if (auto_choose === "false" || auto_choose === "False") {
                            auto_choose = false;
                        }
                        if (auto_choose || (init_value && optionData.value == init_value)) {
                            option.prop('selected', true);
                        }
                        options.push(option);
                    });

                    $selectField.html(options);
                    var width = $selectField.outerWidth();
                    if (navigator.appVersion.indexOf("MSIE") !== -1) {
                        $selectField.width(width + 'px');
                    }

                    $selectField.trigger('change');
                });
            },
            init: function (chainfield, url, id, init_value, empty_label, auto_choose) {
                var val, fill_field = this.fill_field;

                if (!$(chainfield).hasClass("chained")) {
                    val = $(chainfield).val();
                    fill_field(val, init_value, id, url, empty_label, auto_choose);
                }
                $(chainfield).change(function () {
                    // Handle the case of inlines, where the ID will depend on which list item we are dealing with
                    var prefix, start_value, this_val, localID = id;
                    if (localID.indexOf("__prefix__") > -1) {
                        prefix = $(this).attr("id").match(/\d+/)[0];
                        localID = localID.replace("__prefix__", prefix);
                    }

                    start_value = $(localID).val();
                    this_val = $(this).val();
                    fill_field(this_val, start_value, localID, url, empty_label, auto_choose);
                });
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function (win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if (windowname_to_id(win.name) === chainfield) {
                            $(chainfield).change();
                        }
                    };
                }
            }
        };
    }();
}(jQuery || django.jQuery));
