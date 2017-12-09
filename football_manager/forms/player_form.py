from django import forms

class PlayerForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=60)
    date = forms.DateField(input_formats='%m/%d/%Y')
    number = forms.IntegerField(min_value=0, max_value=99)

    def __init__(self, team_list, role_list, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ChoiceField(
            choices=[(team[0], team[1]) for team in team_list]
        )
        self.fields['role'] = forms.ChoiceField(
            choices=[(role[0], role[1]) for role in role_list]
        )
