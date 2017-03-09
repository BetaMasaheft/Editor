from django import forms

class CommitForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={'class': 'form-control input',
                    'placeholder': 'Commit message'}
                )
            )
