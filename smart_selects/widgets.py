from django.conf import settings
from django.forms.widgets import Select
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db.models import get_model

JQUERY_URL = getattr(settings, 'JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')
        
class ChainedSelect(Select):
    def __init__(self, app_name, model_name, chain_field, model_field, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.chain_field = chain_field
        self.model_field = model_field
        super(Select, self).__init__(*args, **kwargs)
        
    class Media:
        js = (
            JQUERY_URL,
        )
    
    def render(self, name, value, attrs=None, choices=()):
        url = "/".join(reverse("chained_filter", kwargs={'app':self.app_name,'model':self.model_name,'field':self.model_field,'value':"1"}).split("/")[:-2])
        js = """
        <script type="text/javascript">
        $(function(){
            var start_value = $("select#id_%(chainfield)s")[0].value
            if($("#%(id)s")[0].value == "" && start_value != ""){
                $.getJSON("%(url)s/"+start_value+"/", function(j){
                    var options = '';
                    options += '<option value="">---------</option>';
                    for (var i = 0; i < j.length; i++) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '</option>';
                    }
                    $("#%(id)s").html(options);
                    $('#%(id)s option:first').attr('selected', 'selected');
                })
            }
            $("select#id_%(chainfield)s").change(function(){
                $.getJSON("%(url)s/"+$(this).val()+"/", function(j){
                    var options = '';
                    options += '<option value="">---------</option>';
                    for (var i = 0; i < j.length; i++) {
                        options += '<option value="' + j[i].value + '">' + j[i].display + '</option>';
                    }
                    $("#%(id)s").html(options);
                    $('#%(id)s option:first').attr('selected', 'selected');
                })
            })
        })
        </script>
        
        """ % {"chainfield":self.chain_field, "url":url, "id":attrs['id']}
        final_choices=[]
        if value:
            item = self.queryset.filter(pk=value)[0]
            pk = getattr(item, self.model_field+"_id")
            filter={self.model_field:pk}
            filtered = get_model( self.app_name, self.model_name).objects.filter(**filter)
            for choice in filtered:
                final_choices.append((choice.pk, unicode(choice)))
        for choice in self.choices:
            self.choices = [choice]
            break
        output = super(ChainedSelect, self).render(name, value, attrs, choices=final_choices)
        output += js
        return mark_safe(output)
