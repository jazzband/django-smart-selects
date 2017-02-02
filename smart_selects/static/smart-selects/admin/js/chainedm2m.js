
(function($) {
    chainedm2m = function() {
        return {
            fireEvent: function(element,event) {
                var evt;
                if (document.createEventObject){
                    // dispatch for IE
                    evt = document.createEventObject();
                    return element.fireEvent('on'+event,evt);
                }
                else{
                    // dispatch for firefox + others
                    evt = document.createEvent("HTMLEvents");
                    evt.initEvent(event, true, true ); // event type,bubbling,cancelable
                    return !element.dispatchEvent(evt);
                }
            },

            dismissRelatedLookupPopup: function(win, chosenId) {
                var name = windowname_to_id(win.name);
                var elem = document.getElementById(name);
                if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                    elem.value += ',' + chosenId;
                } else {
                    elem.value = chosenId;
                }
                fireEvent(elem, 'change');
                win.close();
            },

            fill_field: function(val, initial_value, elem_id, url, initial_parent, auto_choose){
                var $selectField = $(elem_id);
                function trigger_chosen_updated() {
                    if ($.fn.chosen !== undefined) {
                        $selectField.trigger('chosen:updated');
                    }
                }

                if (!val || val === ''){
                    $selectField.html('');
                    trigger_chosen_updated();
                    return;
                }

                // Make sure that these are always an arrays
                val = [].concat(val);
                initial_parent = [].concat(initial_parent);

                var target_url = url + "/" + val + "/";
                var options = [];
                $.getJSON(target_url, function(j){
                    auto_choose = j.length == 1 && auto_choose;

                    var selected_values = {};
                    // if val and initial_parent have any common values, we need to set selected options.
                    if($(val).filter(initial_parent).length >= 0) {
                        for (var i = 0; i < initial_value.length; i++) {
                            selected_values[initial_value[i]] = true;
                        }
                    }

                    // select values which were previously selected (for many2many - many2many chain)
                    $(elem_id + ' option:selected').each(function(){
                        selected_values[$(this).val()] = true;
                    });

                    $.each(j, function (index, optionData) {
                        var option = $('<option></option>')
                            .attr('value', optionData.value)
                            .text(optionData.display);
                        if (auto_choose || selected_values[optionData.value] === true) {
                            option.prop('selected', true);
                        }
                        options.push(option);
                    });

                    $selectField.html(options);
                    var width = $selectField.outerWidth();
                    if (navigator.appVersion.indexOf("MSIE") != -1)
                        $selectField.width(width + 'px');

                    $selectField.trigger('change');

                    trigger_chosen_updated();
                });
            },

            init: function(chainfield, url, id, value, auto_choose) {
                var initial_parent = $(chainfield).val();
                var initial_value = value;

                if(!$(chainfield).hasClass("chained")){
                    var val = $(chainfield).val();
                    this.fill_field(val, initial_value, id, url, initial_parent, auto_choose);
                }
                var fill_field = this.fill_field;
                $(chainfield).change(function(){
                    var localID = id;
                    if (localID.indexOf("__prefix__") > -1) {
                        var prefix = $(this).attr("id").match(/\d+/)[0];
                        localID = localID.replace("__prefix__", prefix);
                    }

                    var start_value = $(localID).val();
                    var val = $(this).val();
                    fill_field(val, initial_value, localID, url, initial_parent, auto_choose);
                });

                // allait en bas, hors du documentready
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function(win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if ("#" + windowname_to_id(win.name) == chainfield) {
                            $(chainfield).change();
                        }
                    };
                }
            }
        };
    }();
})(jQuery || django.jQuery);
