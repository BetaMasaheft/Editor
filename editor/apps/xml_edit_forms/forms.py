from django import forms
from django_ace import AceWidget
from .models import *
from .fields import *

class DynamicForm(forms.Form):
    """ Provides a form which can have extra dynamic fields appended 
    prior to initialisation. """
    dynamic_fields = {}

    def __init__(self):
        super(DynamicForm, self).__init__()
        self.fields.update(self.dynamic_fields)
