from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User, BaseUserManager
from django.contrib.auth.forms import UserCreationForm

from basketball.models import Player, League


class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ['name', 'max_number_teams', 'min_number_players_per_team', 'is_active', 'signup_allowed']


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'age', 'position', 'about', 'leagues']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise ValidationError('Email addresses must be unique.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError('Password must be 6 characters or longer')
        return super(UserForm, self).clean_password()
