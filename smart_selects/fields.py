from django.db.models.fields.related import ForeignKey
from django import forms
from django.forms.models import ModelChoiceField
from django.forms.fields import ChoiceField
from django.forms.widgets import Select
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models.loading import get_model

JQ_URL = getattr(settings, 'JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')

class ChainedForeignKey(ForeignKey):
    """
    chains the choices of a previous combo box with this one
    """
    def __init__(self, to, chained_field, chained_model_field, *args, **kwargs):
        self.app_name = to._meta.app_label
        self.model_name = to._meta.object_name
        self.chain_field = chained_field
        self.model_field = chained_model_field
        ForeignKey.__init__(self, to, *args, **kwargs)
        
        
    def formfield(self, **kwargs):
        defaults = {
            'form_class': ChainedModelChoiceField,
            'queryset': self.rel.to._default_manager.complex_filter(self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            'app_name':self.app_name,
            'model_name':self.model_name,
            'chain_field':self.chain_field,
            'model_field':self.model_field,
        }
        defaults.update(kwargs)
        return super(ChainedForeignKey, self).formfield(**defaults)
        
class ChainedSelect(Select):
    def __init__(self, app_name, model_name, chain_field, model_field, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.chain_field = chain_field
        self.model_field = model_field
        super(Select, self).__init__(*args, **kwargs)
        
    class Media:
        js = (
            JQ_URL,
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


class ChainedModelChoiceField(ModelChoiceField):
    def __init__(self, app_name, model_name, chain_field, model_field, initial=None, *args, **kwargs):
        defaults = {'widget':ChainedSelect(app_name,model_name,chain_field,model_field)}
        defaults.update(kwargs)
        super(ChainedModelChoiceField, self).__init__(initial=initial, *args, **defaults)
    
    #widget = ChainedSelect
    def _get_choices(self):
        self.widget.queryset = self.queryset
        choices = super(ChainedModelChoiceField, self)._get_choices()
        return choices
        if hasattr(self, '_choices'):
            return self._choices
        
        final = [("","---------"),]
        return final
    choices = property(_get_choices, ChoiceField._set_choices)


    
