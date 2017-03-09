from django.db import models
from django import forms
from django.utils.functional import *

from editor.apps.files.models import *

TEXT_GENERATION_FUNCTIONS = ()
EDIT_ACTION_FUNCTIONS = ()

class XMLEditForm(models.Model):
    file_type = models.CharField(max_length=100, choices=tei_file_type_choices())
    form_fields = models.ManyToManyField('XMLEditField')

    def __str__(self):
        return self.file_type

    def generate(self):
        for field in self.form_fields.all():
            print(field) 
        return

class XMLEditField(models.Model):
    text_generation = models.CharField(
            max_length=50,
            help_text="The function used to generate text.",
            choices=TEXT_GENERATION_FUNCTIONS, 
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
        return "{} - {}".format(self.text_generation, self.edit_action)

    def generate(self):
        field = FIELDS[f.field_type]
        return field["field_class"](**field)
