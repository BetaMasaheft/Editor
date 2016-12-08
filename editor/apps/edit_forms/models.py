from django.db import models

from .fields import *

class EditForm(models.Model):
    file_type = models.CharField(max_length=100)
    form_fields = models.ManyToManyField('EditField')

class EditField(models.Model):
    field = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=field_choices)
    config_string = models.CharField(max_length=1000)
