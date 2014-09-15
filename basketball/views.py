from random import shuffle

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, BaseUserManager
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from basketball.models import Player, League, Team, LeagueMembership
from basketball.forms import LeagueForm


def is_superuser(user):
    return user.is_superuser


def leagues(request):
    league_list = League.objects.all()
    context = {'league_list': league_list}
    return render(request, 'basketball/index.html', context)


@user_passes_test(is_superuser)
def create_league(request):
    if request.method == 'GET':
        league_form = LeagueForm()
        context = {'league_form': league_form}
    elif request.method == 'POST':
        league_form = LeagueForm(request.POST)
        if league_form.is_valid():
            league = league_form.save()
            return HttpResponseRedirect(reverse('basketball:league-info', args=[league.pk]))
        else:
            context = {'league_form': league_form}

    return render(request, 'basketball/create_league.html', context)


def league_info(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    context = {'league': league}
    return render(request, 'basketball/league.html', context)


@user_passes_test(is_superuser)
def edit_league_info(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    league_form = LeagueForm(instance=league)
    if request.method == 'POST':
        league_form = LeagueForm(request.POST, instance=league)
        if league_form.is_valid():
            league = league_form.save()
            return HttpResponseRedirect(reverse('basketball:league-info', args=[league.pk]))

    context = {'league_form': league_form, 'league': league}
    return render(request, 'basketball/edit_league.html', context)


@user_passes_test(is_superuser)
def draft_league(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    context = {'league': league}
    if request.method == 'POST':
        result = enact_draft(league)
        if result:
            return result
        context['error'] = True

    return render(request, 'basketball/draft_league.html', context)


def enact_draft(league):
    # Idea is to create a random permutation of players in the league,
    # then assign them to teams, giving the first few teams at most 1 extra player,
    # depending on the number of players registered and minimum number of players per team.
    players = list(league.player_set.all())
    shuffle(players)
    num_players = len(players)
    max_num_teams = league.max_number_teams
    num_teams_possible = num_players / league.min_number_players_per_team
    if num_teams_possible >= max_num_teams:
        num_teams = max_num_teams
    elif num_teams_possible >= 2:
        num_teams = num_teams_possible
    else:
        return None

    num_players_per_equal_team = num_players / num_teams
    num_teams_unequal = num_players % num_teams
    for i in xrange(0, num_teams):
        team_name = 'Team %d' % (i+1)
        team = Team.objects.create(name=team_name, league=league)
        team.save()

        if i < num_teams_unequal:
            start = i*num_players_per_equal_team + i
            end = start + num_players_per_equal_team + 1
        else:
            start = i*num_players_per_equal_team + num_teams_unequal
            end = start + num_players_per_equal_team

        for player in players[start:end]:
            player.assign_to_team_in_league(league, team)

    return HttpResponseRedirect(reverse('basketball:league-info', args=[league.pk]))


@user_passes_test(is_superuser)
def delete_league(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    if request.method == 'POST':
        league.delete()
        return HttpResponseRedirect(reverse('basketball:leagues'))

    context = {'league': league}
    return render(request, 'basketball/delete_league.html', context)


def team_info(request, team_id):
    return HttpResponse('Not implemented yet.')


def player_info(request, player_id):
    return HttpResponse('Not implemented yet.')


def edit_player_info(request, player_id):
    return HttpResponse('Not implemented yet.')


def register(request):
    return HttpResponse('Not implemented yet.')


def login(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated():
            if user.is_superuser:
                return HttpResponseRedirect(reverse('basketball:commissioner-dashboard'))
            else:
                return HttpResponseRedirect(reverse('basketball:edit-player-info', args=[user.player.pk]))
        redirect_next = request.GET.get('next', reverse('basketball:leagues'))
        context = {'error': False, 'next': redirect_next}
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            username = User.objects.get(email=BaseUserManager.normalize_email(username)).get_username
        except User.DoesNotExist:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            redirect_next = request.POST.get('next')
            if not redirect_next:
                redirect_next = reverse('basketball:leagues')
            return HttpResponseRedirect(redirect_next)
        else:
            context = {'error': True}

    return render(request, 'basketball/login.html', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/basketball/')


@user_passes_test(is_superuser)
def commissioner_dashboard(request):
    return render(request, 'basketball/commissioner.html')
