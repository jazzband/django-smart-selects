from django import forms

from .form_fields import ChainedField


class ChainedModelForm(forms.ModelForm):
    
    def clean(self):
        for field_name, field in self.fields.iteritems():
            if issubclass(type(field), ChainedField):
                field.clean_form(field_name, self.cleaned_data)
        return self.cleaned_data
