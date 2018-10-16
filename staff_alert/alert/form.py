from django import forms

class FileUpload(forms.Form):

    file_title = forms.CharField(max_length=50)
    myfile = forms.FileField()
