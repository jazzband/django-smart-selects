
(function($) {
    chainedm2m = function() {
        return {
            fireEvent: function(element,event) {
                if (document.createEventObject){
                    // dispatch for IE
                    var evt = document.createEventObject();
                    return element.fireEvent('on'+event,evt)
                }
                else{
                    // dispatch for firefox + others
                    var evt = document.createEvent("HTMLEvents");
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
                if (!val || val === ''){
                    $(elem_id).html('');
                    return;
                }
                var target_url = url + "/" + val + "/";
                $.getJSON(target_url, function(j){
                    var options = '';

                    for (var i = 0; i < j.length; i++) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '<'+'/option>';
                    }
                    var width = $(elem_id).outerWidth();
                    $(elem_id).html(options);
                    if (navigator.appVersion.indexOf("MSIE") != -1)
                        $(elem_id).width(width + 'px');

                    if(val == initial_parent){
                        for (var i = 0; i < initial_value.length; i++) {
                            $(elem_id + ' option[value="'+ initial_value[i] +'"]').attr('selected', 'selected');
                        }
                    }
                    if(auto_choose && j.length == 1){
                        $(elem_id + ' option[value="'+ j[0].value +'"]').attr('selected', 'selected');
                    }

                    $(elem_id).trigger('change');

                    if ($.fn.chosen !== undefined) {
                        $(elem_id).trigger('chosen:updated');
                    }
                })
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
                    var val = $(this).val();
                    fill_field(val, initial_value, id, url, initial_parent, auto_choose);
                })

                // allait en bas, hors du documentready
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function(win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if ("#" + windowname_to_id(win.name) == chainfield) {
                            $(chainfield).change();
                        }
                    }
                }

            }
        }
    }();
})(jQuery || django.jQuery);
