from django import forms

class BasicXMLForm(forms.Form):
    xml_text = forms.CharField(widget=forms.Textarea)

class NameXMLForm(forms.Form):
    name_field = forms.CharField() 
