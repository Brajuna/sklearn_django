from django import forms

class FileUpload(forms.Form):

    file_title = forms.CharField(max_length=50)
    myfile = forms.FileField()

class Signup(forms.Form):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    user_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

