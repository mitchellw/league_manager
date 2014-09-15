from django.forms import ModelForm

from basketball.models import Player, League


class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ['name', 'max_number_teams', 'min_number_players_per_team', 'is_active', 'signup_allowed']
