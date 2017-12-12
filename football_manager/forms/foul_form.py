from django import forms

class FoulForm(forms.Form):

    minute = forms.IntegerField(min_value=0, max_value=120)

    def __init__(self, card_types, players_list, *args, **kwargs):
        super(FoulForm, self).__init__(*args, **kwargs)
        self.fields['carda'] = forms.ChoiceField(
            choices=[(card, card) for card in card_types]
        )
        self.fields['player'] = forms.ChoiceField(
            choices=[(role[0], role[1]) for role in  players_list]
        )
