from django import forms
from django_ace import AceWidget
from .models import *

ace_options = {
        'theme': 'kuroir', 
        'width': '100%', 
        'height': '600px',
        }

class TextForm(forms.Form):
    text = forms.CharField(widget=AceWidget(mode='text', **ace_options))

class XMLForm(forms.Form):
    text = forms.CharField(widget=AceWidget(mode='xml', **ace_options))

