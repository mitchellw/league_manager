from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
                       # /api/leagues/
                       url(r'^leagues/$', views.leagues, name='leagues'),
                       # /api/leagues/1/
                       url(r'^leagues/(?P<league_id>\d+)/$', views.league_info, name='league-info'),
                       # /api/teams/
                       url(r'^teams/$', views.teams, name='teams'),
                       # /api/teams/1/
                       url(r'^teams/(?P<team_id>\d+)/$', views.team_info, name='team-info'),
                       # /api/players/
                       url(r'^players/$', views.players, name='players'),
                       # /api/players/1/
                       url(r'^players/(?P<player_id>\d+)/$', views.player_info, name='player-info'),
                       )
