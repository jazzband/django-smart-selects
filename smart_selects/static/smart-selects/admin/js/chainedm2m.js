(function ($) {
    "use strict";

    window.chainedm2m = function () {
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

            dismissRelatedLookupPopup: function(win, chosenId) {
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

            fill_field: function (val, initial_value, elem_id, url, initial_parent, auto_choose) {
                var $selectField = $(elem_id),
                    $selectedto = $(elem_id + '_to'),
                    cache_to = elem_id.replace('#', '') + '_to',
                    cache_from = elem_id.replace('#', '') + '_from';
                if (!$selectField.length) {
                    $selectField = $(elem_id + '_from');
                }
                function trigger_chosen_updated() {
                    if ($.fn.chosen !== undefined) {
                        $selectField.trigger('chosen:updated');
                    }
                }

                // SelectBox is a global var from djangojs "admin/js/SelectBox.js"
                // Clear cache to avoid the elements duplication
                if (typeof SelectBox !== 'undefined') {
                    if (typeof SelectBox.cache[cache_to] !== 'undefined') {
                        SelectBox.cache[cache_to].splice(0);
                    }
                    if (typeof SelectBox.cache[cache_from] !== 'undefined') {
                        SelectBox.cache[cache_from].splice(0);
                    }
                }

                if (!val || val === '') {
                    $selectField.html('');
                    $selectedto.html('');
                    trigger_chosen_updated();
                    return;
                }

                // Make sure that these are always an arrays
                val = [].concat(val);
                initial_parent = [].concat(initial_parent);

                var target_url = url + "/" + val + "/",
                    options = [],
                    selectedoptions = [];

                $.getJSON(target_url, function (j) {
                    var i, width;
                    auto_choose = j.length === 1 && auto_choose;

                    var selected_values = {};
                    // if val and initial_parent have any common values, we need to set selected options.
                    if ($(val).filter(initial_parent).length >= 0 && initial_value) {
                        for (i = 0; i < initial_value.length; i = i + 1) {
                            selected_values[initial_value[i]] = true;
                        }
                    }

                    // select values which were previously selected (for many2many - many2many chain)
                    $(elem_id + ' option:selected').each(function () {
                        selected_values[$(this).val()] = true;
                    });

                    $.each(j, function (index, optionData) {
                        var option = $('<option></option>')
                            .attr('value', optionData.value)
                            .text(optionData.display)
                            .attr('title', optionData.display);
                        if (auto_choose === "true" || auto_choose === "True") {
                            auto_choose = true;
                        } else if (auto_choose === "false" || auto_choose === "False") {
                            auto_choose = false;
                        }
                        if (auto_choose || selected_values[optionData.value] === true) {
                            if ($selectedto.length) {
                                selectedoptions.push(option);
                            } else {
                                option.prop('selected', true);
                                options.push(option);
                            }
                        } else {
                            options.push(option);
                        }
                    });

                    $selectField.html(options);
                    if ($selectedto.length) {
                        $selectedto.html(selectedoptions);
                        var node;
                        // SelectBox is a global var from djangojs "admin/js/SelectBox.js"
                        for (i = 0, j = selectedoptions.length; i < j; i = i + 1) {
                            node = selectedoptions[i];
                            SelectBox.cache[cache_to].push({value: node.prop("value"), text: node.prop("text"), displayed: 1});
                        }
                        for (i = 0, j = options.length; i < j; i = i + 1) {
                            node = options[i];
                            SelectBox.cache[cache_from].push({value: node.prop("value"), text: node.prop("text"), displayed: 1});
                        }
                    }
                    width = $selectField.outerWidth();
                    if (navigator.appVersion.indexOf("MSIE") !== -1) {
                        $selectField.width(width + 'px');
                    }

                    $selectField.trigger('change');

                    trigger_chosen_updated();
                });
            },

            init: function (chainfield, url, id, value, auto_choose) {
                var fill_field, val, initial_parent = $(chainfield).val(),
                    initial_value = value;

                if (!$(chainfield).hasClass("chained")) {
                    val = $(chainfield).val();
                    this.fill_field(val, initial_value, id, url, initial_parent, auto_choose);
                }
                fill_field = this.fill_field;
                $(chainfield).change(function () {
                    var prefix, start_value, this_val, localID = id;
                    if (localID.indexOf("__prefix__") > -1) {
                        prefix = $(this).attr("id").match(/\d+/)[0];
                        localID = localID.replace("__prefix__", prefix);
                    }

                    start_value = $(localID).val();
                    this_val = $(this).val();
                    fill_field(this_val, initial_value, localID, url, initial_parent, auto_choose);
                });

                // allait en bas, hors du documentready
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function (win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if ("#" + windowname_to_id(win.name) === chainfield) {
                            $(chainfield).change();
                        }
                    };
                }
                if (typeof(dismissRelatedLookupPopup) !== 'undefined') {
                    var oldDismissRelatedLookupPopup = dismissRelatedLookupPopup;
                    dismissRelatedLookupPopup = function (win, chosenId) {
                        oldDismissRelatedLookupPopup(win, chosenId);
                        if ("#" + windowname_to_id(win.name) === chainfield) {
                            $(chainfield).change();
                        }
                    };
                }
            }
        };
    }();
}(jQuery || django.jQuery));
