from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class League(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    signup_allowed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    league = models.ForeignKey(League, limit_choices_to={'is_active': True})

    def __unicode__(self):
        return self.name


class Player(models.Model):
    GUARD = 'G'
    FORWARD = 'F'
    CENTER = 'C'
    POSITION_CHOICES = (
        (GUARD, 'Guard'),
        (FORWARD, 'Forward'),
        (CENTER, 'Center'),
    )
    position = models.CharField(max_length=1,
                                choices=POSITION_CHOICES,
                                default=GUARD)
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    leagues = models.ManyToManyField(League, through='LeagueMembership')
    user = models.OneToOneField(User)

    # Not required
    about = models.TextField(max_length=250, blank=True)

    def register_for_league(self, league):
        self.assign_to_team_in_league(league, None)

    def assign_to_team_in_league(self, league, team):
        try:
            league_membership = self.leaguemembership_set.get(league=league)
            league_membership.team = team
        except LeagueMembership.DoesNotExist:
            league_membership = LeagueMembership(league=league, player=self, team=team)

        league_membership.save()

    def __unicode__(self):
        return self.name


class LeagueMembership(models.Model):
    league = models.ForeignKey(League)
    player = models.ForeignKey(Player)

    date_joined = models.DateTimeField(auto_now_add=True)

    # Null if Player just signed up for League and hasn't been drafted to a team
    team = models.ForeignKey(Team, null=True, blank=True)
