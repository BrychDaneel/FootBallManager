from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=50)
    city = forms.CharField(max_length=60)
    country = forms.CharField()
    emblem = forms.ImageField()
    arena_name = forms.CharField()
    arena_city = forms.CharField(max_length=60)
    arena_country = forms.CharField()
