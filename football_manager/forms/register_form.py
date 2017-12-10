from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    password_again = forms.CharField()
