from django import forms

class MatchForm(forms.Form):
  
    def __init__(self, team_list, arena_list, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['home_team'] = forms.ChoiceField(
            choices=[(team[0], team[1]) for team in team_list]
        )
        self.fields['guest_team'] = forms.ChoiceField(
            choices=[(team[0], team[1]) for team in team_list]
        )
        self.fields['arena'] = forms.ChoiceField(
            choices=[(team[0], team[1]) for team in arena_list]
        )
    
    def clean(self):
        data = self.cleaned_data
        if data['home_team'] == data['guest_team']:
            raise forms.ValidationError("Some team")
        return data
 
 
