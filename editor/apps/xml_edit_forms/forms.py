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

def pseudo_dynamic_form(typed_file):
    form = forms.Form()
    xpath = "/ns:TEI/ns:text/ns:body/ns:listPlace/ns:place/ns:placeName/text()"
    fields = [StandardCharField('placename', xpath, replace)]
    for f in fields:
        name, field = f.initialise_field(typed_file)
        form.fields[name] = field
    return form
