from django import forms
 
class MediumCreatorForm(forms.Form):
     
    docfile = forms.FileField(
        label='Select a file to upload'
    )
