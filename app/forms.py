from django import forms
from app.models import Person
from dashboard.models import Option, CustomField


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "first_name",
            "middle_name",
            "last_name",
        ]

    def __init__(self, *args, **kwargs):
        organization = kwargs.pop(
            "organization", None
        )  # Expecting organization to be passed
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Standard fields from Person model
        self.fields["first_name"].label = "First Name"
        self.fields["middle_name"].label = "Middle Name"
        self.fields["last_name"].label = "Last Name"
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

        # Dynamically generate fields based on organization's custom fields
        if organization:
            custom_fields = CustomField.objects.filter(organization=organization)
            for custom_field in custom_fields:
                if custom_field.field_type == "Text":
                    self.fields[custom_field.name] = forms.CharField(
                        label=custom_field.name,
                        required=True,
                        widget=forms.TextInput(attrs={"class": "input"}),
                    )
                elif custom_field.field_type == "BigText":
                    self.fields[custom_field.name] = forms.CharField(
                        label=custom_field.name,
                        required=True,
                        widget=forms.Textarea(attrs={"class": "textarea"}),
                    )
                elif custom_field.field_type == "Radio":
                    options = Option.objects.filter(custom_field=custom_field)
                    self.fields[custom_field.name] = forms.ChoiceField(
                        label=custom_field.name,
                        choices=[(option.id, option.option_name) for option in options],
                        widget=forms.RadioSelect,
                    )
                elif custom_field.field_type == "Checkbox":
                    options = Option.objects.filter(custom_field=custom_field)
                    self.fields[custom_field.name] = forms.MultipleChoiceField(
                        label=custom_field.name,
                        choices=[(option.id, option.option_name) for option in options],
                        widget=forms.CheckboxSelectMultiple,
                    )
