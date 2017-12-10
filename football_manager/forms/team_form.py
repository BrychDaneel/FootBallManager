from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=50)
    city = forms.CharField(max_length=60)
    country = forms.CharField()
    emblem = forms.ImageField()

    def __init__(self, arena_list, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['arena'] = forms.ChoiceField(
            choices=[(arena[0], arena[1]) for arena in arena_list]
        )
