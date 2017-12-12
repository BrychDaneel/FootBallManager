from django import forms

class GoalForm(forms.Form):

    minute = forms.IntegerField(min_value=0, max_value=120)

    def __init__(self, players_list, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)

        self.fields['player'] = forms.ChoiceField(
            choices=[(role[0], role[1]) for role in  players_list]
        )
