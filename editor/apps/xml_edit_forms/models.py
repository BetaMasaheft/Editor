from django.db import models
from django import forms
from django.utils.functional import *

from django_ace import AceWidget

from editor.apps.files.models import *

from .fields import *

ace_options = {
        'theme': 'kuroir', 
        'width': '100%', 
        'height': '600px',
        'wordwrap': True,
        }

class XMLEditForm(models.Model):
    form_name = models.CharField(
            max_length=100,
            help_text="A descriptive name for this form.",
            )
    file_type = models.CharField(max_length=100, choices=tei_file_type_choices())
    form_fields = models.ManyToManyField('XMLEditField')

    def __str__(self):
        return "{} - {}".format(
                self.file_type, 
                self.form_name
                )

    def generate_fields(self):
        return (field.generate() for field in self.form_fields.all())

    def create_and_populate(self, typed_file):
        form = forms.Form
        for f in self.generate_fields():
            name, field = f.populate(typed_file)
            #TODO: make sure this isn't a terrible idea
            # the .fields attribute isn't created till the object is initialised
            # where it's created by a deep_copy from .base_fields.
            form.base_fields[name] = field
        return form

    def process_form(self, populated_form, typed_file):
        for name, data in populated_form.cleaned_data.items():
            f = self.form_fields.get(field_name=name).generate()
            typed_file = f.process(typed_file, data)
        return typed_file


class XMLEditField(models.Model):
    field_name = models.CharField(
            max_length=100,
            help_text="A descriptive name for this field.",
            )
    form_field = models.CharField(
            max_length=50,
            help_text="The form field used to generate text.",
            choices=xml_field_choices(), 
            )
    edit_action = models.CharField(
            max_length=50,
            help_text="Whether the generated text should be appended to the node or replace it.",
            choices=EDIT_ACTION_FUNCTIONS, 
            )
    xpath = models.CharField(
            max_length=1000,
            help_text="The XPath at which the node to be edited can be found.",
            )

    def __str__(self):
        return "{} - {}:{}".format(
                self.field_name, 
                self.form_field, 
                self.edit_action 
                )

    def generate(self):
        field = assign_xml_field(self.form_field)
        return field(self.field_name, self.xpath, self.edit_action)

class XMLForm():
    form_name = "xml_form"
    file_type = "*"

    def __str__(self):
        return "{} - {}".format(
                self.file_type, 
                self.form_name
                )

    def create_and_populate(typed_file):
        form = forms.Form
        form.base_fields['text'] = forms.CharField(
                initial=typed_file.text,
                widget=AceWidget(mode='xml', **ace_options)
                )
        return form

    def process_form(populated_form, typed_file):
        typed_file.text = populated_form.cleaned_data['text']
        return typed_file

