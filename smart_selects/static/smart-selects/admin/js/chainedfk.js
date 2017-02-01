(function($) {
    chainedfk = function() {
        return {
            fireEvent: function(element,event){
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
            fill_field: function(val, init_value, elem_id, url, empty_label, auto_choose){
                var $selectField = $(elem_id);
                url = url + "/" + val+ "/";
                if (!val || val === ''){
                    var options = '<option value="">' + empty_label +'</option>';
                    $(elem_id).html(options);
                    $(elem_id + ' option:first').prop('selected', true);
                    $(elem_id).trigger('change');
                    return;
                }
                $.getJSON(url, function(j){
                    // Append empty label as the first option
                    $('<option></option>')
                        .attr('value', '')
                        .text(empty_label)
                        .appendTo($selectField);

                    // Append each option to the select
                    $.each(j, function (index, optionData) {
                        $('<option></option>')
                            .attr('value', optionData.value)
                            .text(optionData.display)
                            .appendTo($selectField);
                    });
                    var width = $(elem_id).outerWidth();
                    if (navigator.appVersion.indexOf("MSIE") != -1)
                        $(elem_id).width(width + 'px');
                    if(init_value){
                        $(elem_id + ' option[value="'+ init_value +'"]').prop('selected', true);
                    } else {
                        $(elem_id + ' option:first').prop('selected', true);
                    }
                    if(auto_choose && j.length == 1){
                        $(elem_id + ' option[value="'+ j[0].value +'"]').prop('selected', true);
                    }
                    $(elem_id).trigger('change');
                });
            },
            init: function(chainfield, url, id, init_value, empty_label, auto_choose) {
                var fill_field = this.fill_field;

                if(!$(chainfield).hasClass("chained")){
                    var val = $(chainfield).val();
                    fill_field(val, init_value, id, url, empty_label, auto_choose);
                }
                $(chainfield).change(function(){
                    // Handle the case of inlines, where the ID will depend on which list item we are dealing with
                    var localID = id;
                    if (localID.indexOf("__prefix__") > -1) {
                        var prefix = $(this).attr("id").match(/\d+/)[0];
                        localID = localID.replace("__prefix__", prefix);
                    }

                    var start_value = $(localID).val();
                    var val = $(this).val();
                    fill_field(val, start_value, localID, url, empty_label, auto_choose);
                });
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function(win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if (windowname_to_id(win.name) == chainfield) {
                            $(chainfield).change();
                        }
                    };
                }
            }
        };
    }();
})(jQuery || django.jQuery);
