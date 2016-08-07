from django import forms

class BasicXMLForm(forms.Form):
    xml_text = forms.CharField(widget=forms.Textarea)
