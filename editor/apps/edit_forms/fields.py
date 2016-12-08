from django import forms

FIELDS = {
    "text": {
        "description": "Single line text",
        "form_class": forms.CharField,
        },
    "textarea": {
        "description": "Multiline text",
        "form_class": forms.CharField,
        "widget": forms.Textarea,
        },
    }

field_choices = ((k, v.get("description")) for k, v in FIELDS.items())

def construct_field(arg1):
    """TODO: Docstring for construct_field.

    :arg1: TODO
    :returns: TODO

    """
    pass
