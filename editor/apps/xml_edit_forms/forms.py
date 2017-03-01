from django import forms
from django_ace import AceWidget
from .models import *
from .fields import *

ace_options = {
        'theme': 'kuroir', 
        'width': '100%', 
        'height': '600px',
        }

class TextForm(forms.Form):
    name = "text_form"
    text = forms.CharField(widget=AceWidget(mode='text', **ace_options))

class XMLForm(forms.Form):
    name = "xml_form"
    text = forms.CharField(widget=AceWidget(mode='xml', **ace_options))

def pseudo_dynamic_form(f):
    form = forms.Form()
    initial_text = f.ns_xpath("/ns:TEI/ns:text/ns:body/ns:listPlace/ns:place/ns:placeName/text()")[0]
    form.fields['placename'] = forms.CharField(initial=initial_text)
    return form
