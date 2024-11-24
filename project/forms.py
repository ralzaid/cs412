from django import forms
from .models import Team, Match

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['player_one', 'player_two', 'score']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['round', 'team_one', 'team_two', 'team_one_score', 'team_two_score']
