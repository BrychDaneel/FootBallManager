from django import forms

class ArenaForm(forms.Form):
    arena_name = forms.CharField()
    city = forms.CharField(max_length=60)
    country = forms.CharField()
