from django import forms
from django_ace import AceWidget
from .models import *
from .fields import *

ace_options = {
        'theme': 'kuroir', 
        'width': '100%', 
        'height': '600px',
        'wordwrap': True,
        }

class TextForm(forms.Form):
    name = "text_form"
    text = forms.CharField(widget=AceWidget(mode='text', **ace_options))

class XMLForm(forms.Form):
    name = "xml_form"
    text = forms.CharField(widget=AceWidget(mode='xml', **ace_options))
