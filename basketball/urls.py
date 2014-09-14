from django.conf.urls import patterns, url

from basketball import views

urlpatterns = patterns('',
                       # /basketball/
                       url(r'^$', views.leagues, name='leagues'),
                       # Commissioner only - /basketball/leagues/create
                       url(r'^leagues/create$', views.create_league, name='create-league'),
                       # /basketball/leagues/1/
                       url(r'^leagues/(?P<league_id>\d+)/$', views.league_info, name='league-info'),
                       # Commissioner only - /basketball/leagues/1/edit
                       url(r'^leagues/(?P<league_id>\d+)/edit$', views.edit_league_info, name='edit-league-info'),
                       # Commissioner only - /basketball/leagues/1/draft
                       url(r'^leagues/(?P<league_id>\d+)/draft$', views.draft_league, name='draft-league'),
                       # Commissioner only - /basketball/leagues/1/delete
                       url(r'^leagues/(?P<league_id>\d+)/delete$', views.delete_league, name='delete-league'),
                       # /basketball/teams/1/
                       url(r'^teams/(?P<team_id>\d+)/$', views.team_info, name='team-info'),
                       # /basketball/players/1/
                       url(r'^players/(?P<player_id>\d+)/$', views.player_info, name='player-info'),
                       # /basketball/players/1/edit
                       url(r'^players/(?P<player_id>\d+)/edit$', views.edit_player_info, name='edit-player-info'),
                       # /basketball/register/
                       url(r'^leagues/register/$', views.register, name='registration'),
                       # /basketball/login/
                       url(r'^leagues/login/$', views.login, name='login'),
                       # Commissioner only - /basketball/commissioner/
                       url(r'^leagues/commissioner/$', views.commissioner_dashboard, name='commissioner-dashboard'),
                       )
