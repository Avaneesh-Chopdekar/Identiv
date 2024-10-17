from django import forms
from .models import CustomField, Option


class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ["name", "field_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "input"})
        self.fields["field_type"].widget.attrs.update({"class": "select"})


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option_name"].widget.attrs.update({"class": "input is-small"})
