(function($) {
    function fireEvent(element,event){
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
    }

    function dismissRelatedLookupPopup(win, chosenId) {
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
            elem.value += ',' + chosenId;
        } else {
            elem.value = chosenId;
        }
        fireEvent(elem, 'change');
        win.close();
    }

    $(document).ready(function(){
        function fill_field(relatedTo, relatedSelect) {
            var init_value = relatedSelect.val();
            var val = relatedTo.val();
            var empty_label = relatedSelect.data('ss-empty_label');
            if (!val || val==''){
                options = '<option value="">'+empty_label+'<'+'/option>';
                relatedSelect.html(options);
                relatedSelect.find('option:first').attr('selected', 'selected');
                relatedSelect.trigger('change');
                return;
            }

            $.getJSON(relatedSelect.data('ss-url') + "/"+val+"/", function(j){
                var options = '<option value="">'+empty_label+'<'+'/option>';
                for (var i = 0; i < j.length; i++) {
                    options += '<option value="' + j[i].value + '">' + j[i].display + '<'+'/option>';
                }
                var width = relatedSelect.outerWidth();
                relatedSelect.html(options);
                if (navigator.appVersion.indexOf("MSIE") != -1)
                    relatedSelect.width(width + 'px');
                var auto_choose = relatedSelect.data('ss-auto_choose');
                if(init_value){
                    relatedSelect.find('option[value="'+ init_value +'"]').attr('selected', 'selected');
                }
                if(auto_choose && j.length == 1){
                    relatedSelect.find('option[value="'+ j[0].value +'"]').attr('selected', 'selected');
                } else if (relatedSelect.find('option[selected=selected]').length === 0) {
                    relatedSelect.find('option:first').attr('selected', 'selected');
                }
                relatedSelect.trigger('change');
            });
        }

        $("#content-main").on('change', 'select', function(){
            var relatedTo = $(this);
            var relatedSelect = $('select.chained[data-ss-id="'+relatedTo.attr('id')+'"]');
            if ( relatedSelect.length == 0 ) return;
            fill_field(relatedTo, relatedSelect);
        });
    });
    if (typeof(dismissAddAnotherPopup) !== 'undefined') {
        var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
        dismissAddAnotherPopup = function(win, newId, newRepr) {
            oldDismissAddAnotherPopup(win, newId, newRepr);
            var id = windowname_to_id(win.name);
            var relatedSelect = $('select.chained[data-ss-id="'+id+'"]');
            if ( relatedSelect.length == 0 ) return;
            $('#' + id).change();
        }
    }
})(jQuery || django.jQuery);

