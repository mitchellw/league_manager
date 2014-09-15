from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, get_list_or_404
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
            return HttpResponseRedirect(reverse('basketball:league-created', args=[league.pk]))
        else:
            context = {'league_form': league_form}

    return render(request, 'basketball/create_league.html', context)


@user_passes_test(is_superuser)
def league_created(request, league_id):
    try:
        league = League.objects.get(pk=league_id)
    except League.DoesNotExist:
        league = None
    context = {'league': league}
    return render(request, 'basketball/league_created.html', context)


def league_info(request, league_id):
    return HttpResponse('Not implemented yet.')


def edit_league_info(request, league_id):
    return HttpResponse('Not implemented yet.')


def draft_league(request, league_id):
    return HttpResponse('Not implemented yet.')


def delete_league(request, league_id):
    return HttpResponse('Not implemented yet.')


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


def commissioner_dashboard(request):
    return HttpResponse('Not implemented yet.')
