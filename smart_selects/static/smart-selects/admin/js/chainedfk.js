(function($) {
    chainedfk = function() {
        return {
            fireEvent: function(element,event){
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
            fill_field: function(val, init_value, elem_id, url, empty_label, auto_choose){
                url = url + "/" + val+ "/";
                if (!val || val==''){
                    var options = '<option value="">' + empty_label +'</option>';
                    $(elem_id).html(options);
                    $(elem_id + ' option:first').attr('selected', 'selected');
                    $(elem_id).trigger('change');
                    return;
                }
                $.getJSON(url, function(j){
                    var options = '<option value="">' + empty_label +'</option>';
                    for (var i = 0; i < j.length; i++) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '<'+'/option>';
                    }
                    var width = $(elem_id).outerWidth();
                    $(elem_id).html(options);
                    if (navigator.appVersion.indexOf("MSIE") != -1)
                        $(elem_id).width(width + 'px');
                    $(elem_id + ' option:first').attr('selected', 'selected');
                    if(init_value){
                        $(elem_id + ' option[value="'+ init_value +'"]').attr('selected', 'selected');
                    }
                    if(auto_choose && j.length == 1){
                        $(elem_id + ' option[value="'+ j[0].value +'"]').attr('selected', 'selected');
                    }
                    $(elem_id).trigger('change');
                })
            },
            init: function(chainfield, url, id, init_value, empty_label, auto_choose) {
                var fill_field = this.fill_field;

                if(!$(chainfield).hasClass("chained")){
                    var val = $(chainfield).val();
                    fill_field(val, init_value, id, url, empty_label, auto_choose);
                }
                $(chainfield).change(function(){
                    var start_value = $(id).val();
                    var val = $(this).val();
                    fill_field(val, start_value, id, url, empty_label, auto_choose);
                })
                if (typeof(dismissAddAnotherPopup) !== 'undefined') {
                    var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
                    dismissAddAnotherPopup = function(win, newId, newRepr) {
                        oldDismissAddAnotherPopup(win, newId, newRepr);
                        if (windowname_to_id(win.name) == chainfield) {
                            $(chainfield).change();
                        }
                    }
                }
            }   
        }
    }();
})(jQuery || django.jQuery);