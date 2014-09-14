from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from basketball.models import Player, League, Team, LeagueMembership


def leagues(request):
    league_list = League.objects.all()
    context = {'league_list': league_list}
    return render(request, 'basketball/index.html', context)


def create_league(request):
    return HttpResponse('Not implemented yet.')


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
    return HttpResponse('Not implemented yet.')


def commissioner_dashboard(request):
    return HttpResponse('Not implemented yet.')
