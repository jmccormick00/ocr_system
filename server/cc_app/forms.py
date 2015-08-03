from django import forms


class UploadFileForm(forms.Form):
    description = forms.CharField(max_length=200)
    #file = forms.FileField()
