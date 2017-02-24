from django.db import models
from django import forms

FIELDS = {
    "text": {
        "description": "Single line text",
        "field_class": forms.CharField,
        },
    "textarea": {
        "description": "Multiline text",
        "field_class": forms.CharField,
        "widget": forms.Textarea,
        },
    }

field_choices = ((k, v.get("description")) for k, v in FIELDS.items())

class XMLEditForm(models.Model):
    file_type = models.CharField(max_length=100)
    form_fields = models.ManyToManyField('XMLEditField')

    def __str__(self):
        return self.file_type

class XMLEditField(models.Model):
    text_generation = models.CharField(max_length=50)
    edit_action = models.CharField(max_length=50)
    xpath = models.CharField(max_length=1000)

    def __str__(self):
        return "{} - {}".format(self.field, self.config_string)

    def create(self):
        field = FIELDS[f.field_type]
        return field["field_class"](**field)
